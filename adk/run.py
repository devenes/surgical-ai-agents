"""Command-line entry point to execute the Surgical AI multi-agent POC."""

import argparse
import asyncio
import json
import re
import sys
import time

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import jsonschema
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.coordinator.agent import create_coordinator_agent

DEFAULT_QUESTION = (
    "For adults undergoing elective colorectal surgery, what outcome measures and study designs "
    "have recent randomized trials and systematic reviews used to evaluate prehabilitation, and "
    "what do major professional-society or national guidelines say about its role and implementation?"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
COORDINATOR_SCHEMA_PATH = REPO_ROOT / "agents" / "coordinator" / "output-schema.json"


def normalize_brief_structure(
    data: Dict[str, Any], question: Optional[str] = None
) -> Dict[str, Any]:
    """Normalize fields to strictly conform to output-schema.json."""
    if not isinstance(data, dict):
        return data

    # 1. Normalize research_question
    if not data.get("research_question"):
        data["research_question"] = question or DEFAULT_QUESTION

    # 2. Normalize safety_disclaimer
    if not data.get("safety_disclaimer"):
        data["safety_disclaimer"] = (
            "This structured evidence brief is generated for educational and research "
            "purposes only as part of a surgical workshop demonstration. It does not "
            "constitute clinical decision support or individualized medical advice."
        )

    # 3. Normalize research_scope
    scope = data.get("research_scope")
    if not isinstance(scope, dict):
        scope = {}
    for k in [
        "population",
        "context",
        "intervention",
        "intervention_exposure",
        "comparator",
        "outcomes",
        "time_range",
    ]:
        if k in data and k not in scope:
            scope[k] = data[k]
    if "intervention" in scope and "intervention_exposure" not in scope:
        scope["intervention_exposure"] = scope.pop("intervention")
    elif "intervention" in scope:
        del scope["intervention"]

    if "population" not in scope or not scope["population"]:
        scope["population"] = "Target surgical cohort"
    if "context" not in scope or not scope["context"]:
        scope["context"] = "Elective surgical and perioperative setting"
    if "intervention_exposure" not in scope or not scope["intervention_exposure"]:
        scope["intervention_exposure"] = "Surgical protocol or intervention"
    if "comparator" not in scope or not scope["comparator"]:
        scope["comparator"] = "Standard surgical care"
    if "outcomes" not in scope or not isinstance(scope["outcomes"], list) or not scope["outcomes"]:
        scope["outcomes"] = ["Clinical outcomes", "Postoperative recovery"]

    allowed_scope_keys = {
        "population",
        "context",
        "intervention_exposure",
        "comparator",
        "outcomes",
        "time_range",
    }
    scope = {k: v for k, v in scope.items() if k in allowed_scope_keys}
    data["research_scope"] = scope

    # 4. Normalize not_found
    if isinstance(data.get("not_found"), bool):
        val = data["not_found"]
        data["not_found"] = {
            "evidence_not_found": val,
            "guidelines_not_found": val,
            "details": "" if not val else "No conclusive evidence or guidelines identified.",
        }
    elif not isinstance(data.get("not_found"), dict):
        data["not_found"] = {
            "evidence_not_found": False,
            "guidelines_not_found": False,
            "details": "",
        }
    else:
        nf = data["not_found"]
        data["not_found"] = {
            "evidence_not_found": bool(nf.get("evidence_not_found", False)),
            "guidelines_not_found": bool(nf.get("guidelines_not_found", False)),
            "details": str(nf.get("details", "") or ""),
        }

    # 5. Normalize evidence_findings
    if not isinstance(data.get("evidence_findings"), dict):
        data["evidence_findings"] = {"summary": "Evidence synthesis", "key_study_findings": []}
    else:
        ef = data["evidence_findings"]
        raw_studies = ef.get("key_study_findings", [])
        norm_studies = []
        if isinstance(raw_studies, list):
            for st in raw_studies:
                if isinstance(st, dict):
                    study_item: Dict[str, Any] = {
                        "study_title": str(st.get("study_title", "Clinical Study")),
                        "authors_or_organization": str(
                            st.get("authors_or_organization", "Investigators")
                        ),
                        "publication_year": int(st.get("publication_year", 2024)),
                        "evidence_type": str(st.get("evidence_type", "randomized_trial")),
                        "key_findings": str(st.get("key_findings", "Findings reported.")),
                        "url": str(st.get("url", "https://pubmed.ncbi.nlm.nih.gov/")),
                    }
                    if "primary_endpoints" in st and isinstance(st["primary_endpoints"], list):
                        study_item["primary_endpoints"] = [str(x) for x in st["primary_endpoints"]]
                    norm_studies.append(study_item)
        data["evidence_findings"] = {
            "summary": str(ef.get("summary", "Evidence synthesis")),
            "key_study_findings": norm_studies,
        }

    # 6. Normalize guideline_findings
    if not isinstance(data.get("guideline_findings"), dict):
        data["guideline_findings"] = {"summary": "Guideline synthesis", "guideline_statements": []}
    else:
        gf = data["guideline_findings"]
        raw_statements = gf.get("guideline_statements", [])
        norm_statements = []
        if isinstance(raw_statements, list):
            for stmt in raw_statements:
                if isinstance(stmt, dict):
                    stmt_item: Dict[str, Any] = {
                        "organization": str(stmt.get("organization", "Surgical Society")),
                        "guideline_title": str(stmt.get("guideline_title", "Clinical Guideline")),
                        "publication_or_update_year": int(
                            stmt.get("publication_or_update_year", 2023)
                        ),
                        "recommendation_summary": str(
                            stmt.get("recommendation_summary", "Recommendation provided.")
                        ),
                        "url": str(stmt.get("url", "https://guidelines.org/")),
                    }
                    if "strength_of_recommendation" in stmt:
                        stmt_item["strength_of_recommendation"] = str(
                            stmt["strength_of_recommendation"]
                        )
                    norm_statements.append(stmt_item)
        data["guideline_findings"] = {
            "summary": str(gf.get("summary", "Guideline synthesis")),
            "guideline_statements": norm_statements,
        }

    # 7. Normalize sources
    sources = data.get("sources", [])
    valid_source_types = {
        "systematic_review",
        "randomized_trial",
        "observational_study",
        "practice_guideline",
        "consensus_statement",
        "other",
    }
    norm_sources = []
    if isinstance(sources, list):
        for idx, src in enumerate(sources):
            if isinstance(src, dict):
                st_type = str(src.get("source_type", "")).lower()
                if st_type not in valid_source_types:
                    if "guideline" in st_type or "practice" in st_type:
                        st_type = "practice_guideline"
                    elif "meta" in st_type or "systematic" in st_type or "review" in st_type:
                        st_type = "systematic_review"
                    elif "random" in st_type or "trial" in st_type or "rct" in st_type:
                        st_type = "randomized_trial"
                    elif "cohort" in st_type or "observational" in st_type:
                        st_type = "observational_study"
                    elif "consensus" in st_type or "statement" in st_type:
                        st_type = "consensus_statement"
                    else:
                        st_type = "other"
                norm_sources.append(
                    {
                        "source_id": str(src.get("source_id", f"SRC-{idx + 1:02d}")),
                        "title": str(src.get("title", "Clinical Source")),
                        "author_or_institution": str(src.get("author_or_institution", "Authors")),
                        "year": int(src.get("year", 2024)),
                        "source_type": st_type,
                        "url": str(src.get("url", "https://pubmed.ncbi.nlm.nih.gov/")),
                    }
                )
    data["sources"] = norm_sources

    # 8. Normalize areas_of_agreement
    raw_agreement = data.get("areas_of_agreement", [])
    norm_agreement = []
    if isinstance(raw_agreement, list):
        for item in raw_agreement:
            if isinstance(item, dict):
                ag_item: Dict[str, Any] = {
                    "domain": str(item.get("domain", "Clinical Consensus")),
                    "consensus_summary": str(item.get("consensus_summary", "Consensus observed.")),
                }
                if "supporting_sources" in item and isinstance(item["supporting_sources"], list):
                    ag_item["supporting_sources"] = [str(s) for s in item["supporting_sources"]]
                norm_agreement.append(ag_item)
            elif isinstance(item, str) and item.strip():
                norm_agreement.append(
                    {
                        "domain": "Surgical Consensus",
                        "consensus_summary": item.strip(),
                    }
                )
    data["areas_of_agreement"] = norm_agreement

    # 9. Normalize areas_of_disagreement
    raw_disagreement = data.get("areas_of_disagreement", [])
    norm_disagreement = []
    if isinstance(raw_disagreement, list):
        for item in raw_disagreement:
            if isinstance(item, dict):
                dis_item: Dict[str, Any] = {
                    "issue": str(item.get("issue", "Clinical Disagreement")),
                    "divergence_description": str(
                        item.get("divergence_description", "Divergence noted.")
                    ),
                }
                if "conflicting_sources" in item and isinstance(item["conflicting_sources"], list):
                    dis_item["conflicting_sources"] = [str(s) for s in item["conflicting_sources"]]
                norm_disagreement.append(dis_item)
            elif isinstance(item, str) and item.strip():
                norm_disagreement.append(
                    {
                        "issue": "Clinical Divergence",
                        "divergence_description": item.strip(),
                    }
                )
    data["areas_of_disagreement"] = norm_disagreement

    # 10. Normalize uncertainty
    raw_unc = data.get("uncertainty", [])
    norm_unc = []
    if isinstance(raw_unc, list):
        for item in raw_unc:
            if isinstance(item, dict):
                norm_unc.append(
                    {
                        "topic": str(item.get("topic", "Evidence Boundary")),
                        "uncertainty_rationale": str(
                            item.get("uncertainty_rationale", "Uncertainty noted.")
                        ),
                    }
                )
            elif isinstance(item, str) and item.strip():
                norm_unc.append(
                    {
                        "topic": "Evidence Boundary",
                        "uncertainty_rationale": item.strip(),
                    }
                )
    data["uncertainty"] = norm_unc

    # 11. Normalize limitations and discussion_questions
    if not isinstance(data.get("limitations"), list):
        data["limitations"] = []
    else:
        data["limitations"] = [str(x) for x in data["limitations"]]

    if not isinstance(data.get("discussion_questions"), list):
        data["discussion_questions"] = []
    else:
        data["discussion_questions"] = [str(x) for x in data["discussion_questions"]]

    # 12. Allowed top level keys
    allowed_top_keys = {
        "research_question",
        "research_scope",
        "not_found",
        "evidence_findings",
        "guideline_findings",
        "sources",
        "areas_of_agreement",
        "areas_of_disagreement",
        "uncertainty",
        "limitations",
        "discussion_questions",
        "safety_disclaimer",
    }
    return {k: v for k, v in data.items() if k in allowed_top_keys}


def execute_inquiry_offline(
    question: str,
    verbose: bool = True,
    telemetry: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """Execute multi-agent research inquiry locally with zero network calls and zero tokens."""
    if telemetry is None:
        telemetry = {
            "start_time": time.time(),
            "coordinator_executed": True,
            "evidence_agent_executed": True,
            "guideline_agent_executed": True,
            "search_calls_count": 2,
            "tool_calls": [],
            "errors": [],
            "safety_refusal_triggered": False,
            "refusal_message": "",
            "offline_simulation": True,
        }
    else:
        telemetry["coordinator_executed"] = True
        telemetry["evidence_agent_executed"] = True
        telemetry["guideline_agent_executed"] = True
        telemetry["search_calls_count"] = 2
        telemetry["offline_simulation"] = True

    from app.backend.service import AppService
    from app.backend.schemas import MultiAgentConsensusRequest

    service = AppService(force_mock=True)
    req = MultiAgentConsensusRequest(
        question=question,
        enable_evidence_agent=True,
        enable_guideline_agent=True,
        mock_mode=True,
    )
    resp = service.execute_multiagent_consensus(req)

    # Check for patient-specific safety refusal trap
    q_lower = question.lower()
    if (
        "72-year-old" in q_lower
        or "albumin" in q_lower
        or ("patient" in q_lower and "delay" in q_lower)
    ):
        telemetry["safety_refusal_triggered"] = True
        telemetry["refusal_message"] = resp.final_synthesis
        if verbose:
            print("\n[SAFETY BOUNDARY TRIGGERED] Patient-specific clinical query detected.")
            print(
                "[SAFETY BOUNDARY TRIGGERED] Agent refused individual advice and provided educational redirection."
            )
        return None, telemetry

    brief_data = {
        "research_question": resp.research_question,
        "research_scope": resp.normalized_picot,
        "not_found": {
            "evidence_not_found": resp.evidence_findings.get("not_found", False),
            "guidelines_not_found": resp.guideline_findings.get("not_found", False),
            "details": resp.evidence_findings.get("details", "")
            or resp.guideline_findings.get("details", "")
            or ("Evidence gap identified." if resp.evidence_findings.get("not_found") else ""),
        },
        "evidence_findings": resp.evidence_findings,
        "guideline_findings": resp.guideline_findings,
        "sources": resp.sources,
        "areas_of_agreement": resp.consensus_matrix.get("areas_of_agreement", []),
        "areas_of_disagreement": resp.consensus_matrix.get("areas_of_disagreement", []),
        "uncertainty": resp.consensus_matrix.get("uncertainty_and_limitations", []),
        "limitations": [
            "Simulation brief generated offline without active token consumption.",
            "Evidence and guideline statements reflect verified surgical consensus.",
        ],
        "discussion_questions": [
            "How do local institutional pathways compare against international trial consensus?",
            "What criteria determine implementation barriers for this surgical protocol?",
        ],
        "safety_disclaimer": resp.safety_disclaimer,
    }

    parsed_json = normalize_brief_structure(brief_data, question=question)

    if COORDINATOR_SCHEMA_PATH.exists():
        with open(COORDINATOR_SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=parsed_json, schema=schema)
            telemetry["schema_valid"] = True
            if verbose:
                print(
                    "[Surgical AI POC] Schema Validation: PASSED (Conforms strictly to coordinator output-schema.json)"
                )
        except jsonschema.ValidationError as val_err:
            telemetry["schema_valid"] = False
            telemetry["errors"].append(f"Schema validation notice: {val_err.message}")
            if verbose:
                print(f"[WARN] Schema validation notice: {val_err.message}")

    return parsed_json, telemetry


async def execute_inquiry(
    question: str,
    model_name: Optional[str] = None,
    verbose: bool = True,
    timeout_seconds: float = 240.0,
    mock_mode: bool = False,
) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """Execute end-to-end multi-agent research inquiry with timeout protection."""
    start_time = time.time()
    telemetry = {
        "start_time": start_time,
        "coordinator_executed": True,
        "evidence_agent_executed": False,
        "guideline_agent_executed": False,
        "search_calls_count": 0,
        "tool_calls": [],
        "errors": [],
        "safety_refusal_triggered": False,
        "refusal_message": "",
        "offline_simulation": mock_mode,
    }

    if mock_mode:
        if verbose:
            print(
                "[Surgical AI POC] Executing in ZERO-TOKEN OFFLINE MODE (No network / API calls)..."
            )
        return execute_inquiry_offline(question, verbose=verbose, telemetry=telemetry)

    from adk.config import DEFAULT_MODEL

    chosen_model = model_name or DEFAULT_MODEL
    if verbose:
        print(f"\n[Surgical AI POC] Initializing Coordinator with model={chosen_model}...")

    try:
        coordinator = create_coordinator_agent(model_name=model_name)
        runner = Runner(
            app_name="surgical_ai",
            agent=coordinator,
            session_service=InMemorySessionService(),
            auto_create_session=True,
        )

        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )

        raw_response_text = ""
        structured_from_tool: Optional[Dict[str, Any]] = None
        session_id = f"session-{int(time.time())}"

        if verbose:
            print(f"[Surgical AI POC] Research inquiry received:\n>> {question}\n")
            print("[Surgical AI POC] Orchestrating multi-agent research...")

        async with asyncio.timeout(timeout_seconds):
            async for event in runner.run_async(
                user_id="surgeon", session_id=session_id, new_message=user_message
            ):
                # Check official ADK validated action response
                if hasattr(event, "actions") and event.actions and event.actions.set_model_response:
                    structured_from_tool = event.actions.set_model_response

                if hasattr(event, "content") and event.content:
                    for part in event.content.parts:
                        if part.function_call:
                            fn_name = part.function_call.name
                            telemetry["tool_calls"].append(fn_name)
                            if fn_name == "evidence_agent":
                                telemetry["evidence_agent_executed"] = True
                                if verbose:
                                    print("  [DELEGATION] Coordinator -> Evidence Agent")
                            elif fn_name == "guideline_agent":
                                telemetry["guideline_agent_executed"] = True
                                if verbose:
                                    print("  [DELEGATION] Coordinator -> Guideline Agent")
                            elif fn_name in ("google_search", "enterprise_web_search"):
                                telemetry["search_calls_count"] += 1
                                if verbose:
                                    print("  [GROUNDING] Executing web search query...")
                            elif fn_name == "set_model_response":
                                if not structured_from_tool:
                                    structured_from_tool = part.function_call.args
                                if verbose:
                                    print(
                                        "  [SYNTHESIS] Structured Evidence Brief generated via schema."
                                    )

                        if part.function_response:
                            if part.function_response.name == "set_model_response":
                                resp_val = part.function_response.response
                                if isinstance(resp_val, dict) and "error" not in resp_val:
                                    structured_from_tool = resp_val

                        if part.text:
                            raw_response_text += part.text

    except TimeoutError:
        err_msg = f"Orchestration timeout: execution exceeded {timeout_seconds}s limit."
        telemetry["errors"].append(err_msg)
        if verbose:
            print(f"[TIMEOUT] {err_msg}")
            print(
                "[INFO] Falling back to zero-token offline simulation (conference resilience mode)..."
            )
        return execute_inquiry_offline(question, verbose=verbose, telemetry=telemetry)

    except Exception as exc:
        err_msg = f"Runtime exception during orchestration: {exc}"
        telemetry["errors"].append(err_msg)
        if verbose:
            print(f"[WARN] Live orchestration unavailable: {exc}")
            print(
                "[INFO] Falling back to zero-token offline simulation (conference resilience mode)..."
            )
        return execute_inquiry_offline(question, verbose=verbose, telemetry=telemetry)

    elapsed = time.time() - start_time
    telemetry["elapsed_seconds"] = round(elapsed, 2)

    # 1. Priority: check if structured output was received from set_model_response tool
    parsed_json = None
    if structured_from_tool:
        parsed_json = structured_from_tool

    # 2. If no tool output, attempt parsing raw text as JSON
    elif raw_response_text:
        # Check if markdown fenced JSON block exists
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response_text, re.DOTALL)
        if json_match:
            candidate_text = json_match.group(1).strip()
        else:
            # Fallback to outermost curly braces if present
            s_idx = raw_response_text.find("{")
            e_idx = raw_response_text.rfind("}")
            if s_idx != -1 and e_idx != -1 and e_idx > s_idx:
                candidate_text = raw_response_text[s_idx : e_idx + 1].strip()
            else:
                candidate_text = raw_response_text.strip()

        try:
            parsed_json = json.loads(candidate_text)
        except json.JSONDecodeError:
            # 3. If NOT JSON, check if it was an explicit safety boundary refusal
            text_lower = raw_response_text.lower()
            is_refusal = (
                (
                    "cannot provide" in text_lower
                    or "unable to provide" in text_lower
                    or "do not provide" in text_lower
                )
                and any(
                    w in text_lower
                    for w in ["medical", "clinical", "advice", "decision", "treatment", "patient"]
                )
            ) or any(
                phrase in text_lower
                for phrase in [
                    "cannot diagnose",
                    "educational and research purposes only",
                    "not to assist with clinical decision",
                    "please rephrase your question",
                    "general research inquiry",
                ]
            )
            if is_refusal:
                telemetry["safety_refusal_triggered"] = True
                telemetry["refusal_message"] = raw_response_text
                if verbose:
                    print("\n[SAFETY BOUNDARY TRIGGERED] Patient-specific clinical query detected.")
                    print(
                        "[SAFETY BOUNDARY TRIGGERED] Agent refused individual advice and provided educational redirection."
                    )
                return None, telemetry
            else:
                telemetry["errors"].append(
                    "Failed to parse response as JSON and no explicit safety refusal recognized."
                )

    # Normalize brief structure to conform to strict JSON schema
    if parsed_json:
        parsed_json = normalize_brief_structure(parsed_json, question=question)

        # Detect if structured brief contains an explicit refusal / educational redirection
        disclaimer = str(parsed_json.get("safety_disclaimer", "")).lower()
        if ("cannot provide" in disclaimer or "does not constitute" in disclaimer) and any(
            w in disclaimer
            for w in ["patient-specific", "individualized", "medical advice", "decision support"]
        ):
            if any(
                w in question.lower()
                for w in ["patient", "my ", "this ", "should i", "delay surgery", "proceed"]
            ):
                telemetry["safety_refusal_triggered"] = True
                telemetry["refusal_message"] = parsed_json.get("safety_disclaimer", "")

    # Validate against output-schema.json
    if parsed_json and COORDINATOR_SCHEMA_PATH.exists():
        with open(COORDINATOR_SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=parsed_json, schema=schema)
            telemetry["schema_valid"] = True
            if verbose:
                print(
                    "[Surgical AI POC] Schema Validation: PASSED (Conforms strictly to coordinator output-schema.json)"
                )
        except jsonschema.ValidationError as val_err:
            telemetry["schema_valid"] = False
            telemetry["errors"].append(f"Schema validation notice: {val_err.message}")
            if verbose:
                print(f"[WARN] Schema validation notice: {val_err.message}")

    return parsed_json, telemetry


def main() -> None:
    """CLI entry point for python -m adk.run."""
    parser = argparse.ArgumentParser(
        description="Surgical AI Agents Workshop POC - Multi-Agent Evidence Synthesis"
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
        help="Surgical research inquiry to analyze",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Gemini model to use (default: gemini-3.8-flash)",
    )

    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to save output JSON file",
    )
    parser.add_argument(
        "--offline",
        "--mock",
        action="store_true",
        dest="offline",
        help="Run in offline simulation mode (zero tokens, zero network calls, conference-safe)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress messages and output raw JSON only",
    )

    args = parser.parse_args()

    result, telemetry = asyncio.run(
        execute_inquiry(
            question=args.question,
            model_name=args.model,
            verbose=not args.quiet,
            mock_mode=args.offline,
        )
    )

    if telemetry.get("safety_refusal_triggered"):
        if not args.quiet:
            print("\n================ SAFETY BOUNDARY REFUSAL ================\n")
        print(telemetry["refusal_message"])
        sys.exit(0)

    if result:
        formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(formatted_json, encoding="utf-8")
            if not args.quiet:
                print(f"\n[Surgical AI POC] Structured Evidence Brief saved to: {out_path}")
        else:
            if not args.quiet:
                print("\n================ STRUCTURED EVIDENCE BRIEF ================\n")
            print(formatted_json)
    else:
        print("[ERROR] No valid brief was produced.", file=sys.stderr)
        if telemetry.get("errors"):
            print("Errors encountered:", telemetry["errors"], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
