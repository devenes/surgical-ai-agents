"""Command-line entry point to execute the Surgical AI multi-agent POC."""

import argparse
import asyncio
import json
import re
import sys
import time
import traceback

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

    # Normalize research_question
    if not data.get("research_question"):
        data["research_question"] = question or DEFAULT_QUESTION

    # Normalize safety_disclaimer
    if not data.get("safety_disclaimer"):
        data["safety_disclaimer"] = (
            "This structured evidence brief is generated for educational and research "
            "purposes only as part of a surgical workshop demonstration. It does not "
            "constitute clinical decision support or individualized medical advice."
        )

    # Normalize research_scope
    if not isinstance(data.get("research_scope"), dict) or not data["research_scope"].get(
        "population"
    ):
        scope = data.get("research_scope") if isinstance(data.get("research_scope"), dict) else {}
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
            scope["intervention_exposure"] = scope["intervention"]
        if "population" not in scope:
            scope["population"] = "Target surgical cohort"
        if "context" not in scope:
            scope["context"] = "Elective surgical setting"
        if "intervention_exposure" not in scope:
            scope["intervention_exposure"] = "Surgical protocol"
        if "comparator" not in scope:
            scope["comparator"] = "Standard care"
        if "outcomes" not in scope:
            scope["outcomes"] = ["Clinical outcomes"]
        data["research_scope"] = scope

    # Normalize not_found if model provided a bare boolean
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

    # Normalize container lists and dicts
    if not isinstance(data.get("evidence_findings"), dict):
        data["evidence_findings"] = {"summary": "Evidence synthesis", "key_study_findings": []}
    if not isinstance(data.get("guideline_findings"), dict):
        data["guideline_findings"] = {"summary": "Guideline synthesis", "guideline_statements": []}
    if not isinstance(data.get("sources"), list):
        data["sources"] = []
    if not isinstance(data.get("areas_of_agreement"), list):
        data["areas_of_agreement"] = []
    if not isinstance(data.get("areas_of_disagreement"), list):
        data["areas_of_disagreement"] = []
    if not isinstance(data.get("uncertainty"), list):
        data["uncertainty"] = []
    if not isinstance(data.get("limitations"), list):
        data["limitations"] = []
    if not isinstance(data.get("discussion_questions"), list):
        data["discussion_questions"] = []

    # Normalize source_type enum values
    sources = data.get("sources", [])
    valid_types = {
        "systematic_review",
        "randomized_trial",
        "observational_study",
        "practice_guideline",
        "consensus_statement",
        "other",
    }
    if isinstance(sources, list):
        for src in sources:
            if isinstance(src, dict):
                st = str(src.get("source_type", "")).lower()
                if st not in valid_types:
                    if "guideline" in st or "practice" in st:
                        src["source_type"] = "practice_guideline"
                    elif "meta" in st or "systematic" in st or "review" in st:
                        src["source_type"] = "systematic_review"
                    elif "random" in st or "trial" in st or "rct" in st:
                        src["source_type"] = "randomized_trial"
                    elif "cohort" in st or "observational" in st:
                        src["source_type"] = "observational_study"
                    elif "consensus" in st or "statement" in st:
                        src["source_type"] = "consensus_statement"
                    else:
                        src["source_type"] = "other"

    # Remove any unexpected top-level keys that violate additionalProperties: false
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
    for k in list(data.keys()):
        if k not in allowed_top_keys:
            del data[k]

    return data


async def execute_inquiry(
    question: str,
    model_name: Optional[str] = None,
    verbose: bool = True,
    timeout_seconds: float = 240.0,
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
    }

    from adk.config import DEFAULT_MODEL

    chosen_model = model_name or DEFAULT_MODEL
    if verbose:
        print(f"\n[Surgical AI POC] Initializing Coordinator with model={chosen_model}...")

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

    try:
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

    except Exception as exc:
        err_msg = f"Runtime exception during orchestration: {exc}"
        telemetry["errors"].append(err_msg)
        if verbose:
            print(f"[ERROR] {err_msg}")
            traceback.print_exc()

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
