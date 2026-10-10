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
from app.frontend.i18n import SUPPORTED_LOCALES, get_locale, set_locale, t


def render_sidebar_controls(models: List[ModelInfo]) -> Dict[str, Any]:
    """Render unified sidebar controls for model selection, tokens, and agents."""
    st.sidebar.title(t("sidebar.title"))

    # 0. Language Selector (Persistent via session state)
    current_locale = get_locale()
    locale_options = list(SUPPORTED_LOCALES)
    selected_locale = st.sidebar.selectbox(
        t("sidebar.language"),
        options=locale_options,
        index=locale_options.index(current_locale) if current_locale in locale_options else 0,
        format_func=lambda code: "English" if code == "en" else "Türkçe",
        key="locale_selector",
    )
    if selected_locale != current_locale:
        set_locale(selected_locale)

    # 1. Primary Model Selection
    model_ids = [m.id for m in models]
    model_dict = {m.id: m for m in models}

    def format_model(mid: str) -> str:
        m = model_dict.get(mid)
        return m.display_name if m else mid

    selected_model_id = st.sidebar.selectbox(
        t("sidebar.model_label"),
        options=model_ids,
        format_func=format_model,
        index=0,
        help=t("sidebar.model_help"),
    )

    selected_model_info = model_dict[selected_model_id]
    st.sidebar.caption(f"ℹ️ {selected_model_info.description}")

    # 2. Reasoning & Thinking Controls
    st.sidebar.markdown(t("sidebar.thinking_heading"))
    thinking_level: Optional[str] = None
    thinking_budget: Optional[int] = None

    if selected_model_info.supports_thinking_level:
        # Native Gemini 3.8+ thinking levels
        level_options = ["MEDIUM", "LOW", "HIGH", "MINIMAL", "Off"]
        selected_level = st.sidebar.selectbox(
            t("sidebar.thinking_level_label"),
            options=level_options,
            index=0,
            help=t("sidebar.thinking_level_help_38"),
        )
        if selected_level != "Off":
            thinking_level = selected_level
        st.sidebar.caption(t("sidebar.thinking_native_active"))

    elif selected_model_info.supports_thinking_budget:
        # Gemini 2.5 series uses token budget; selectable thinking_level maps safely to token budget
        level_options = ["Off / Default", "LOW", "MEDIUM", "HIGH", "MINIMAL"]
        selected_level = st.sidebar.selectbox(
            t("sidebar.thinking_level_label"),
            options=level_options,
            index=0,
            help=t("sidebar.thinking_level_help_25"),
        )
        if selected_level != "Off / Default":
            thinking_level = selected_level

        tb_mode = st.sidebar.selectbox(
            t("sidebar.thinking_budget_mode_label"),
            ["Auto", "Manual", "Off"],
            format_func=lambda m: t(f"sidebar.tb_modes.{m}"),
            index=0,
            help=t("sidebar.thinking_budget_mode_help"),
        )
        if tb_mode == "Manual":
            thinking_budget = st.sidebar.slider(
                t("sidebar.thinking_budget_tokens_label"),
                min_value=128,
                max_value=16384,
                value=2048,
                step=128,
                help=t("sidebar.thinking_budget_tokens_help"),
            )
        elif tb_mode == "Off":
            thinking_budget = 0
            thinking_level = None
        elif thinking_level:
            level_map = {"MINIMAL": 512, "LOW": 1024, "MEDIUM": 2048, "HIGH": 4096}
            thinking_budget = level_map.get(thinking_level, 2048)
            st.sidebar.caption(
                t(
                    "sidebar.thinking_mapped_caption",
                    thinking_level=thinking_level,
                    thinking_budget=thinking_budget,
                )
            )
        else:
            st.sidebar.caption(t("sidebar.thinking_vertex_caption"))
    else:
        st.sidebar.selectbox(
            t("sidebar.thinking_level_label"),
            options=[t("sidebar.not_supported")],
            index=0,
            disabled=True,
            help=t("sidebar.thinking_level_help_unsupported"),
        )
        st.sidebar.caption(t("sidebar.thinking_unsupported"))

    # 3. Simulation / Offline Mode Toggle
    mock_mode = st.sidebar.toggle(
        t("sidebar.offline_toggle_label"),
        value=True,
        help=t("sidebar.offline_toggle_help"),
    )
    if not mock_mode:
        st.sidebar.caption(t("sidebar.live_enabled_warning"))

    # 4. Sub-Agent Selection
    st.sidebar.markdown(t("sidebar.subagent_heading"))
    enable_evidence = st.sidebar.toggle(
        t("sidebar.evidence_specialist_label"),
        value=True,
        help=t("sidebar.evidence_specialist_help"),
    )
    enable_guideline = st.sidebar.toggle(
        t("sidebar.guideline_specialist_label"),
        value=True,
        help=t("sidebar.guideline_specialist_help"),
    )

    # 5. Advanced & Backend Settings (Progressive Disclosure)
    with st.sidebar.expander(t("sidebar.advanced_expander"), expanded=False):
        raw_connection_modes = ["Direct In-Process", "FastAPI Backend (REST)"]
        connection_mode = st.radio(
            t("sidebar.execution_mode_label"),
            raw_connection_modes,
            format_func=lambda m: t("sidebar.connection_modes.direct")
            if m == "Direct In-Process"
            else t("sidebar.connection_modes.rest"),
            index=0,
            help=t("sidebar.execution_mode_help"),
        )

        fastapi_url = "http://127.0.0.1:8000"
        if connection_mode == "FastAPI Backend (REST)":
            fastapi_url = st.text_input(
                t("sidebar.fastapi_url_label"),
                value="http://127.0.0.1:8000",
                help=t("sidebar.fastapi_url_help"),
            )

        st.markdown(t("sidebar.hyperparameters_heading"))
        temperature = st.slider(
            t("sidebar.temperature_label"),
            min_value=0.0,
            max_value=2.0,
            value=selected_model_info.default_temperature,
            step=0.05,
        )
        top_p = st.slider(t("sidebar.top_p_label"), min_value=0.0, max_value=1.0, value=0.95, step=0.05)
        max_output_tokens = st.slider(
            t("sidebar.max_output_tokens_label"),
            min_value=256,
            max_value=8192,
            value=2048,
            step=256,
        )

    return {
        "connection_mode": connection_mode,
        "fastapi_url": fastapi_url,
        "mock_mode": mock_mode,
        "model_id": selected_model_id,
        "model_info": selected_model_info,
        "thinking_level": thinking_level,
        "thinking_budget": thinking_budget,
        "temperature": temperature,
        "top_p": top_p,
        "max_output_tokens": max_output_tokens,
        "enable_evidence": enable_evidence,
        "enable_guideline": enable_guideline,
    }


def render_execution_timeline(steps: List[SubAgentExecutionStep]) -> None:
    """Render a visual step-by-step progress timeline for multi-agent execution."""
    st.markdown(t("timeline.title"))

    cols = st.columns(len(steps)) if steps else []
    for i, step in enumerate(steps):
        with cols[i]:
            status_icon = (
                "✅" if step.status == "completed" else ("⏭️" if step.status == "skipped" else "⏳")
            )
            step_label = t("timeline.step", number=i + 1)
            st.markdown(
                f"""
                <div style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; background: #fafafa; margin-bottom: 8px;">
                    <div style="font-weight: 600; font-size: 0.9em;">{status_icon} {step_label}</div>
                    <div style="color: #0366d6; font-size: 0.85em;">{step.agent_name}</div>
                    <div style="font-size: 0.75em; color: #666;">{step.duration_ms:.0f} ms</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander(t("timeline.view_logs"), expanded=False):
        for step in steps:
            st.markdown(
                f"**{step.agent_name}** (`{step.step_type}`) — *{step.status}* ({step.duration_ms:.1f}ms)"
            )
            st.caption(step.summary)
            if step.details:
                st.json(step.details)


def render_consensus_matrix(matrix: Dict[str, Any]) -> None:
    """Render structured consensus, disagreement, and uncertainty matrix."""
    st.markdown(t("matrix.title"))

    agreements = matrix.get("areas_of_agreement", [])
    disagreements = matrix.get("areas_of_disagreement", [])
    uncertainties = matrix.get("uncertainty_and_limitations", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(t("matrix.high_consensus"))
        if agreements:
            for item in agreements:
                st.markdown(f"- {item}")
        else:
            st.caption(t("matrix.no_consensus"))

    with col2:
        st.warning(t("matrix.discrepancy"))
        if disagreements:
            for item in disagreements:
                st.markdown(f"- {item}")
        else:
            st.caption(t("matrix.no_divergence"))

    with col3:
        st.info(t("matrix.uncertainty"))
        if uncertainties:
            for item in uncertainties:
                st.markdown(f"- {item}")
        else:
            st.caption(t("matrix.no_limitations"))


def render_evidence_vs_guidelines(evidence: Dict[str, Any], guidelines: Dict[str, Any]) -> None:
    """Render side-by-side comparison of empirical literature vs society guidelines."""
    st.markdown(t("evidence_vs_guidelines.title"))

    col_ev, col_gd = st.columns(2)

    with col_ev:
        st.subheader(t("evidence_vs_guidelines.evidence_title"))
        ev_summary = evidence.get("summary", t("evidence_vs_guidelines.no_evidence_summary"))
        st.markdown(f"*{ev_summary}*")

        studies = evidence.get("key_study_findings", [])
        if studies:
            st.markdown(t("evidence_vs_guidelines.key_trials"))
            for s in studies:
                title = s.get("study_title", "Untitled Study")
                authors = s.get("authors", "")
                year = s.get("year", "")
                etype = s.get("evidence_type", "")
                findings = s.get("findings", "")
                url = s.get("url", "#")

                with st.container():
                    st.markdown(f"**[{title}]({url})**")
                    tier_text = t("evidence_vs_guidelines.tier", etype=etype)
                    st.caption(f"👤 {authors} ({year}) | {tier_text}")
                    st.markdown(f"> {findings}")
                    st.divider()
        else:
            st.caption(t("evidence_vs_guidelines.no_studies"))

    with col_gd:
        st.subheader(t("evidence_vs_guidelines.guideline_title"))
        gd_summary = guidelines.get("summary", t("evidence_vs_guidelines.no_guideline_summary"))
        st.markdown(f"*{gd_summary}*")

        stmts = guidelines.get("guideline_statements", [])
        if stmts:
            st.markdown(t("evidence_vs_guidelines.society_recs"))
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
                        grade_text = t("evidence_vs_guidelines.grade", grade=grade)
                        st.caption(grade_text)
                    st.markdown(f"> {rec}")
                    st.divider()
        else:
            st.caption(t("evidence_vs_guidelines.no_guidelines"))


def get_case_type_badge(case_type: str) -> str:
    """Return an emoji and label for a clinical case category."""
    badge = t(f"badges.{case_type}")
    if badge != f"badges.{case_type}":
        return badge
    return f"🏷️ {case_type}"


def render_comparative_scorecard(scorecards: List[ComparativeAuditScorecard]) -> None:
    """Render head-to-head 5-dimension clinical AI audit scorecard."""
    st.markdown(t("scorecard.title"))
    st.caption(t("scorecard.caption"))

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
                    for bad in [
                        "High Risk",
                        "Violated",
                        "Ungrounded",
                        "Unstructured",
                        "Missing",
                        "None",
                        "Yüksek Risk",
                        "İhlal",
                        "Dayanaksız",
                        "Eksik",
                        "Yok",
                    ]
                ):
                    st.error(f"❌ {item.without_agent_rating}")
                elif any(
                    warn in item.without_agent_rating
                    for warn in [
                        "Moderate",
                        "Partial",
                        "Generic",
                        "Orta",
                        "Kısmi",
                        "Genel",
                    ]
                ):
                    st.warning(f"⚠️ {item.without_agent_rating}")
                else:
                    st.info(item.without_agent_rating)
            with col_w:
                if any(
                    good in item.with_agent_rating
                    for good in [
                        "Low",
                        "Enforced",
                        "Grounded",
                        "High",
                        "Present",
                        "Verified",
                        "100%",
                        "Düşük",
                        "Uygulandı",
                        "Dayanaklı",
                        "Mevcut",
                        "Doğrulandı",
                    ]
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
    st.markdown(t("side_by_side.title"))

    col_mono, col_agent = st.columns(2)

    with col_mono:
        st.markdown(t("side_by_side.mono_title"))
        st.caption(t("side_by_side.mono_caption", model=without_agent.model, ms=without_agent.latency_ms))

        # Risk indicator pills
        hr_label = t("side_by_side.hallucination_risk")
        gs_label = t("side_by_side.grounding_status")
        sb_label = t("side_by_side.safety_boundary")
        st.markdown(
            f"""
            <div style="background-color: #ffeef0; border-left: 4px solid #cf222e; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px; font-size: 0.85em;">
                <div><b>{hr_label}</b> {without_agent.hallucination_risk}</div>
                <div><b>{gs_label}</b> {without_agent.grounding_status}</div>
                <div><b>{sb_label}</b> {without_agent.safety_boundary_status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if without_agent.key_flaws_noted:
            st.markdown(t("side_by_side.flaws_title"))
            for flaw in without_agent.key_flaws_noted:
                st.markdown(f"- 🔴 {flaw}")

        st.markdown(t("side_by_side.mono_output"))
        with st.container():
            st.markdown(without_agent.raw_response)

        if without_agent.citations_audited:
            with st.expander(t("side_by_side.audited_citations")):
                for cit in without_agent.citations_audited:
                    st.markdown(f"- ⚠️ {cit}")

    with col_agent:
        st.markdown(t("side_by_side.agent_title"))
        st.caption(t("side_by_side.agent_caption", ms=with_agent.latency_ms))

        # Safety & Grounding indicator pills
        gp_text = t("side_by_side.grounding_pill")
        sp_text = t("side_by_side.safety_pill")
        src_text = t("side_by_side.sources_pill", count=len(with_agent.sources))
        st.markdown(
            f"""
            <div style="background-color: #e6ffed; border-left: 4px solid #2da44e; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px; font-size: 0.85em;">
                <div>{gp_text}</div>
                <div>{sp_text}</div>
                <div>{src_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Normalized PICOT
        picot = with_agent.normalized_picot
        if picot and "P" in picot:
            with st.expander(t("side_by_side.picot_title"), expanded=False):
                st.markdown(f"- **P (Population):** {picot.get('P', '')}")
                st.markdown(f"- **I (Intervention):** {picot.get('I', '')}")
                st.markdown(f"- **C (Comparator):** {picot.get('C', '')}")
                st.markdown(
                    f"- **O (Outcomes):** {', '.join(picot.get('O', [])) if isinstance(picot.get('O'), list) else picot.get('O', '')}"
                )
                st.markdown(f"- **T (Time):** {picot.get('T', '')}")

        st.markdown(t("side_by_side.agent_synthesis"))
        with st.container():
            st.markdown(with_agent.final_synthesis)

        if with_agent.sources:
            with st.expander(t("side_by_side.verified_sources", count=len(with_agent.sources))):
                for s in with_agent.sources:
                    title = s.get("title", "")
                    url = s.get("url", "#")
                    stype = s.get("type", "source")
                    st.markdown(f"- `[{stype}]` [{title}]({url})")
