"""Reusable Streamlit UI components and layout helpers for Surgical AI Studio."""

from typing import Any, Dict, List, Optional
import streamlit as st

from app.backend.schemas import (
    ComparativeAuditScorecard,
    ModelInfo,
    MonolithicDirectResponse,
    MultiAgentConsensusResponse,
    SubAgentExecutionStep,
)


def render_sidebar_controls(models: List[ModelInfo]) -> Dict[str, Any]:
    """Render unified sidebar controls for model selection, tokens, and agents."""
    st.sidebar.title("🎛️ Control Panel")

    # 1. Backend connection mode
    connection_mode = st.sidebar.radio(
        "Execution Mode:",
        ["Direct In-Process", "FastAPI Backend (REST)"],
        index=0,
        help="Direct runs in-process with local AppService. REST queries FastAPI at http://127.0.0.1:8000.",
    )

    fastapi_url = "http://127.0.0.1:8000"
    if connection_mode == "FastAPI Backend (REST)":
        fastapi_url = st.sidebar.text_input(
            "FastAPI URL:",
            value="http://127.0.0.1:8000",
            help="Base URL of the running FastAPI server.",
        )

    # 2. Offline / Token-Saver Mode toggle
    mock_mode = st.sidebar.checkbox(
        "⚡ Zero-Token Offline Mode",
        value=True,
        help="Returns high-fidelity deterministic responses with ZERO external API calls and ZERO token usage.",
    )
    if mock_mode:
        st.sidebar.caption("🟢 *Offline mode active: 0 API tokens will be consumed.*")
    else:
        st.sidebar.caption("⚠️ *Live Vertex AI / Gemini API calls enabled.*")

    st.sidebar.divider()

    # 3. Model Selection
    model_ids = [m.id for m in models]
    model_dict = {m.id: m for m in models}

    def format_model(mid: str) -> str:
        m = model_dict.get(mid)
        return m.display_name if m else mid

    selected_model_id = st.sidebar.selectbox(
        "Select Model:",
        options=model_ids,
        format_func=format_model,
        index=0,
        help="Choose Gemini model variant.",
    )

    selected_model_info = model_dict[selected_model_id]
    st.sidebar.caption(f"ℹ️ {selected_model_info.description}")

    # 4. Thinking Budget (if supported)
    thinking_budget: Optional[int] = None
    if selected_model_info.supports_thinking:
        tb_mode = st.sidebar.selectbox(
            "Thinking Budget Mode:",
            ["Auto", "Manual", "Off"],
            index=0,
            help="Configures reasoning / thinking token budget for Gemini 2.5/3.8 series.",
        )
        if tb_mode == "Manual":
            thinking_budget = st.sidebar.slider(
                "Thinking Budget Tokens:",
                min_value=128,
                max_value=16384,
                value=2048,
                step=128,
            )
        elif tb_mode == "Off":
            thinking_budget = 0

    # 5. Generation Parameters
    with st.sidebar.expander("⚙️ Advanced Hyperparameters", expanded=False):
        temperature = st.slider(
            "Temperature (Randomness):",
            min_value=0.0,
            max_value=2.0,
            value=selected_model_info.default_temperature,
            step=0.05,
        )
        top_p = st.slider("Top-P:", min_value=0.0, max_value=1.0, value=0.95, step=0.05)
        max_output_tokens = st.slider(
            "Max Output Tokens:",
            min_value=256,
            max_value=8192,
            value=2048,
            step=256,
        )

    st.sidebar.divider()

    # 6. Sub-Agent Selection
    st.sidebar.markdown("### 🤖 Multi-Agent Configuration")
    enable_evidence = st.sidebar.toggle(
        "Sub-Agent 1: Evidence Specialist",
        value=True,
        help="Searches peer-reviewed trials and systematic reviews (PubMed / Google Search).",
    )
    enable_guideline = st.sidebar.toggle(
        "Sub-Agent 2: Guideline Specialist",
        value=True,
        help="Searches professional surgical society recommendations (ASCRS, ERAS, SAGES).",
    )

    return {
        "connection_mode": connection_mode,
        "fastapi_url": fastapi_url,
        "mock_mode": mock_mode,
        "model_id": selected_model_id,
        "model_info": selected_model_info,
        "thinking_budget": thinking_budget,
        "temperature": temperature,
        "top_p": top_p,
        "max_output_tokens": max_output_tokens,
        "enable_evidence": enable_evidence,
        "enable_guideline": enable_guideline,
    }


def render_execution_timeline(steps: List[SubAgentExecutionStep]) -> None:
    """Render a visual step-by-step progress timeline for multi-agent execution."""
    st.markdown("#### ⏱️ Multi-Agent Execution Pipeline")

    cols = st.columns(len(steps)) if steps else []
    for i, step in enumerate(steps):
        with cols[i]:
            status_icon = (
                "✅" if step.status == "completed" else ("⏭️" if step.status == "skipped" else "⏳")
            )
            st.markdown(
                f"""
                <div style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; background: #fafafa; margin-bottom: 8px;">
                    <div style="font-weight: 600; font-size: 0.9em;">{status_icon} Step {i + 1}</div>
                    <div style="color: #0366d6; font-size: 0.85em;">{step.agent_name}</div>
                    <div style="font-size: 0.75em; color: #666;">{step.duration_ms:.0f} ms</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("🔍 View Detailed Step Logs", expanded=False):
        for step in steps:
            st.markdown(
                f"**{step.agent_name}** (`{step.step_type}`) — *{step.status}* ({step.duration_ms:.1f}ms)"
            )
            st.caption(step.summary)
            if step.details:
                st.json(step.details)


def render_consensus_matrix(matrix: Dict[str, Any]) -> None:
    """Render structured consensus, disagreement, and uncertainty matrix."""
    st.markdown("### ⚖️ Cross-Specialist Consensus & Discrepancy Matrix")

    agreements = matrix.get("areas_of_agreement", [])
    disagreements = matrix.get("areas_of_disagreement", [])
    uncertainties = matrix.get("uncertainty_and_limitations", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("**🟢 High Consensus & Alignment**")
        if agreements:
            for item in agreements:
                st.markdown(f"- {item}")
        else:
            st.caption("No explicit consensus noted.")

    with col2:
        st.warning("**🟡 Clinical Discrepancy / Divergence**")
        if disagreements:
            for item in disagreements:
                st.markdown(f"- {item}")
        else:
            st.caption("No significant divergence detected.")

    with col3:
        st.info("**⚪ Clinical Uncertainty & Limitations**")
        if uncertainties:
            for item in uncertainties:
                st.markdown(f"- {item}")
        else:
            st.caption("No critical limitations reported.")


def render_evidence_vs_guidelines(evidence: Dict[str, Any], guidelines: Dict[str, Any]) -> None:
    """Render side-by-side comparison of empirical literature vs society guidelines."""
    st.markdown("### 📑 Side-by-Side Specialist Findings")

    col_ev, col_gd = st.columns(2)

    with col_ev:
        st.subheader("📚 Evidence Specialist (Sub-Agent 1)")
        ev_summary = evidence.get("summary", "No evidence summary available.")
        st.markdown(f"*{ev_summary}*")

        studies = evidence.get("key_study_findings", [])
        if studies:
            st.markdown("**Key Randomized Trials & Systematic Reviews:**")
            for s in studies:
                title = s.get("study_title", "Untitled Study")
                authors = s.get("authors", "")
                year = s.get("year", "")
                etype = s.get("evidence_type", "")
                findings = s.get("findings", "")
                url = s.get("url", "#")

                with st.container():
                    st.markdown(f"**[{title}]({url})**")
                    st.caption(f"👤 {authors} ({year}) | 📊 Tier: *{etype}*")
                    st.markdown(f"> {findings}")
                    st.divider()
        else:
            st.caption("No individual studies extracted.")

    with col_gd:
        st.subheader("📋 Guideline Specialist (Sub-Agent 2)")
        gd_summary = guidelines.get("summary", "No guideline summary available.")
        st.markdown(f"*{gd_summary}*")

        stmts = guidelines.get("guideline_statements", [])
        if stmts:
            st.markdown("**Official Surgical Society Recommendations:**")
            for g in stmts:
                org = g.get("organization", "Surgical Society")
                title = g.get("guideline_title", "Guideline")
                year = g.get("year", "")
                rec = g.get("recommendation", "")
                grade = g.get("grade", "")
                url = g.get("url", "#")

                with st.container():
                    st.markdown(f"**🏛️ {org} ({year}) — [{title}]({url})**")
                    if grade:
                        st.caption(f"🏅 Recommendation Grade: `{grade}`")
                    st.markdown(f"> {rec}")
                    st.divider()
        else:
            st.caption("No individual society guidelines extracted.")


def get_case_type_badge(case_type: str) -> str:
    """Return an emoji and label for a clinical case category."""
    mapping = {
        "normal_synthesis": "📘 Normal Evidence Synthesis",
        "missing_evidence": "🔍 Edge: Missing Empirical Literature",
        "missing_guideline": "📜 Edge: Missing Society Guideline",
        "evidence_conflict": "⚡ Edge: Evidence vs Guideline Conflict",
        "safety_refusal": "🛑 Safety: Direct Patient Refusal Trap",
    }
    return mapping.get(case_type, f"🏷️ {case_type}")


def render_comparative_scorecard(scorecards: List[ComparativeAuditScorecard]) -> None:
    """Render head-to-head 5-dimension clinical AI audit scorecard."""
    st.markdown("### 📊 Head-to-Head Architectural Audit Scorecard")
    st.caption("Standardized evaluation across 5 critical surgical AI reliability dimensions:")

    for item in scorecards:
        with st.container():
            col_dim, col_wo, col_w = st.columns([1.5, 1.25, 1.25])
            with col_dim:
                st.markdown(f"**{item.dimension}**")
                st.caption(item.explanation)
            with col_wo:
                # Color code without agent
                if any(
                    bad in item.without_agent_rating
                    for bad in ["High Risk", "Violated", "Ungrounded", "Unstructured", "Missing"]
                ):
                    st.error(f"❌ {item.without_agent_rating}")
                elif any(
                    warn in item.without_agent_rating for warn in ["Moderate", "Partial", "Generic"]
                ):
                    st.warning(f"⚠️ {item.without_agent_rating}")
                else:
                    st.info(item.without_agent_rating)
            with col_w:
                if any(
                    good in item.with_agent_rating
                    for good in ["Low", "Enforced", "Grounded", "High", "Present", "Verified"]
                ):
                    st.success(f"✅ {item.with_agent_rating}")
                else:
                    st.info(f"ℹ️ {item.with_agent_rating}")
            st.divider()


def render_direct_vs_agent_side_by_side(
    without_agent: MonolithicDirectResponse,
    with_agent: MultiAgentConsensusResponse,
) -> None:
    """Render side-by-side comparative inspection between Monolithic and Multi-Agent."""
    st.markdown("### ⚖️ Architectural Execution Comparison")

    col_mono, col_agent = st.columns(2)

    with col_mono:
        st.markdown("#### ❌ Monolithic LLM Baseline *(Zero-Shot, No Tools)*")
        st.caption(
            f"🤖 Model: `{without_agent.model}` | ⏱️ Latency: `{without_agent.latency_ms:.0f} ms`"
        )

        # Risk indicator pills
        st.markdown(
            f"""
            <div style="background-color: #ffeef0; border-left: 4px solid #cf222e; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px; font-size: 0.85em;">
                <div><b>⚠️ Hallucination Risk:</b> {without_agent.hallucination_risk}</div>
                <div><b>🌐 Grounding Status:</b> {without_agent.grounding_status}</div>
                <div><b>🛡️ Safety Boundary:</b> {without_agent.safety_boundary_status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if without_agent.key_flaws_noted:
            st.markdown("**Identified Clinical & Rigor Flaws:**")
            for flaw in without_agent.key_flaws_noted:
                st.markdown(f"- 🔴 {flaw}")

        st.markdown("**Monolithic Output:**")
        with st.container():
            st.markdown(without_agent.raw_response)

        if without_agent.citations_audited:
            with st.expander("🔎 Audited Citations in Baseline Output"):
                for cit in without_agent.citations_audited:
                    st.markdown(f"- ⚠️ {cit}")

    with col_agent:
        st.markdown("#### 🛡️ Multi-Agent Architecture *(Coordinator + 2 Specialists)*")
        st.caption(
            f"🤖 Coordinator + Specialists | ⏱️ Pipeline Latency: `{with_agent.latency_ms:.0f} ms`"
        )

        # Safety & Grounding indicator pills
        st.markdown(
            f"""
            <div style="background-color: #e6ffed; border-left: 4px solid #2da44e; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px; font-size: 0.85em;">
                <div><b>✅ Grounding:</b> Dual-specialist empirical & guideline retrieval</div>
                <div><b>🛡️ Safety Guardrail:</b> Automatic educational refusal enforced</div>
                <div><b>📚 Verified Sources:</b> {len(with_agent.sources)} verified literature & guidelines</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Normalized PICOT
        picot = with_agent.normalized_picot
        if picot and "P" in picot:
            with st.expander("📋 Verified PICOT Decomposition", expanded=False):
                st.markdown(f"- **P (Population):** {picot.get('P', '')}")
                st.markdown(f"- **I (Intervention):** {picot.get('I', '')}")
                st.markdown(f"- **C (Comparator):** {picot.get('C', '')}")
                st.markdown(
                    f"- **O (Outcomes):** {', '.join(picot.get('O', [])) if isinstance(picot.get('O'), list) else picot.get('O', '')}"
                )
                st.markdown(f"- **T (Time):** {picot.get('T', '')}")

        st.markdown("**Synthesized Multi-Agent Consensus:**")
        with st.container():
            st.markdown(with_agent.final_synthesis)

        if with_agent.sources:
            with st.expander(
                f"📚 Verified Sources & Evidentiary Citations ({len(with_agent.sources)})"
            ):
                for s in with_agent.sources:
                    t = s.get("title", "")
                    u = s.get("url", "#")
                    stype = s.get("type", "source")
                    st.markdown(f"- `[{stype}]` [{t}]({u})")
