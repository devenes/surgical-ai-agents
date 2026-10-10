"""Streamlit Main Application for Surgical AI Studio (FastAPI + Streamlit).

Supports multimodal image understanding and a 2-subagent (Evidence & Guideline)
orchestration pipeline with token-optimized offline mode and interactive tabs.
Localized for English (en) and Türkçe (tr).
"""

import base64
import io
import mimetypes
import os
from typing import Any, Optional
import httpx
from PIL import Image
import streamlit as st

from app.backend.schemas import (
    ComparativeAnalysisRequest,
    ComparativeAnalysisResponse,
    MonolithicDirectRequest,
    MonolithicDirectResponse,
    MultiAgentConsensusRequest,
    MultiAgentConsensusResponse,
    MultimodalInquiryRequest,
    MultimodalInquiryResponse,
    PICOTDecomposeRequest,
)
from app.backend.service import AppService
from app.frontend.components import (
    get_case_type_badge,
    render_comparative_scorecard,
    render_consensus_matrix,
    render_direct_vs_agent_side_by_side,
    render_evidence_vs_guidelines,
    render_execution_timeline,
    render_sidebar_controls,
)
from app.frontend.i18n import (
    apply_language_directive,
    get_locale,
    get_localized_preset_image,
    get_localized_preset_inquiry,
    get_localized_preset_video,
    get_preset_question_for_locale,
    t,
)

# Page configuration
st.set_page_config(
    page_title=t("app.page_title"),
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Local service instance for direct in-process execution
@st.cache_resource
def get_local_service() -> AppService:
    return AppService()


local_service = get_local_service()
models = local_service.get_models()
preset_questions, preset_images = local_service.get_presets()
preset_videos = local_service.get_preset_videos()

# Sidebar Controls (includes persistent language selector)
params = render_sidebar_controls(models)
current_locale = get_locale()
prev_locale = st.session_state.get("_last_locale", "en")


# Helper: Execute multimodal via REST or direct service
def run_multimodal(req: MultimodalInquiryRequest) -> MultimodalInquiryResponse:
    if params["connection_mode"] == "FastAPI Backend (REST)":
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{params['fastapi_url']}/api/multimodal",
                    json=req.model_dump(),
                )
                resp.raise_for_status()
                return MultimodalInquiryResponse.model_validate(resp.json())
        except Exception as e:
            st.warning(t("warnings.fastapi_fallback", e=e))
    return local_service.execute_multimodal(req)


# Helper: Execute multi-agent consensus via REST or direct service
def run_multiagent(req: MultiAgentConsensusRequest) -> MultiAgentConsensusResponse:
    if params["connection_mode"] == "FastAPI Backend (REST)":
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(
                    f"{params['fastapi_url']}/api/agents/consensus",
                    json=req.model_dump(),
                )
                resp.raise_for_status()
                return MultiAgentConsensusResponse.model_validate(resp.json())
        except Exception as e:
            st.warning(t("warnings.fastapi_fallback", e=e))
    return local_service.execute_multiagent_consensus(req)


# Helper: Execute head-to-head comparative analysis
def run_comparative_analysis(req: ComparativeAnalysisRequest) -> ComparativeAnalysisResponse:
    if params["connection_mode"] == "FastAPI Backend (REST)":
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(
                    f"{params['fastapi_url']}/api/agents/compare",
                    json=req.model_dump(),
                )
                resp.raise_for_status()
                return ComparativeAnalysisResponse.model_validate(resp.json())
        except Exception as e:
            st.warning(t("warnings.fastapi_fallback", e=e))
    return local_service.execute_comparative_analysis(req)


# Helper: Execute monolithic direct query
def run_monolithic_direct(req: MonolithicDirectRequest) -> MonolithicDirectResponse:
    if params["connection_mode"] == "FastAPI Backend (REST)":
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{params['fastapi_url']}/api/agents/direct",
                    json=req.model_dump(),
                )
                resp.raise_for_status()
                return MonolithicDirectResponse.model_validate(resp.json())
        except Exception as e:
            st.warning(t("warnings.fastapi_fallback", e=e))
    return local_service.execute_monolithic_direct(req)


# =============================================================================
# Main Header
# =============================================================================
st.header(t("header.title"), divider="rainbow")
mode_text = t("header.offline_mode") if params["mock_mode"] else t("header.live_mode")
agents_count = int(params["enable_evidence"]) + int(params["enable_guideline"])
thinking_desc = params.get("thinking_level") or (
    t("header.tokens_unit", budget=params["thinking_budget"])
    if params.get("thinking_budget") is not None
    else t("header.default_value")
)
st.caption(
    f"🧠 **{t('header.model')}:** `{params['model_info'].display_name}` &nbsp;•&nbsp; "
    f"💭 **{t('header.thinking')}:** `{thinking_desc}` &nbsp;•&nbsp; "
    f"🔌 **{t('header.mode')}:** `{mode_text}` &nbsp;•&nbsp; "
    f"🤖 **{t('header.subagents')}:** `{t('header.active_count', count=agents_count)}` &nbsp;•&nbsp; "
    f"⚙️ **{t('header.backend')}:** `{params['connection_mode']}`"
)


# =============================================================================
# Application Tabs
# =============================================================================
tab_research, tab_multimodal, tab_diagnostics = st.tabs(
    [
        t("tabs.research"),
        t("tabs.multimodal"),
        t("tabs.diagnostics"),
    ]
)


# -----------------------------------------------------------------------------
# TAB 1: Clinical Research & Consensus
# -----------------------------------------------------------------------------
with tab_research:
    research_mode_keys = [
        "multi_agent_consensus",
        "benchmark_audit",
        "picot_decomposer",
        "specialist_deep_dive",
    ]
    research_mode = st.segmented_control(
        "Research Workflow:",
        options=research_mode_keys,
        format_func=lambda m: t(f"research.modes.{m}"),
        default="multi_agent_consensus",
        label_visibility="collapsed",
    )

    # 1. Primary Multi-Agent Consensus Mode
    if research_mode == "multi_agent_consensus":
        st.subheader(t("research.consensus.subheader"))
        st.caption(t("research.consensus.caption"))

        preset_q_ids = [p.id for p in preset_questions]

        def format_preset_qid(qid: str) -> str:
            raw_p = next(p for p in preset_questions if p.id == qid)
            loc_p = get_localized_preset_inquiry(raw_p, current_locale)
            return f"{loc_p.title} ({loc_p.category})"

        selected_preset_qid = st.selectbox(
            t("research.consensus.preset_label"),
            options=preset_q_ids,
            format_func=format_preset_qid,
            key="ma_preset_select",
        )

        raw_active_preset = next(p for p in preset_questions if p.id == selected_preset_qid)
        active_preset = get_localized_preset_inquiry(raw_active_preset, current_locale)
        st.caption(
            f"{get_case_type_badge(raw_active_preset.case_type)} — *{active_preset.pedagogical_lesson}*"
        )

        # Smart prompt management: preserve user edits, update on preset or locale switch if unedited
        prev_qid = st.session_state.get("_last_ma_preset_id", selected_preset_qid)
        if selected_preset_qid != prev_qid:
            st.session_state["ma_question_input"] = active_preset.question
            st.session_state["_last_ma_preset_id"] = selected_preset_qid
        elif current_locale != prev_locale:
            prev_question = get_preset_question_for_locale(
                selected_preset_qid, prev_locale, raw_active_preset.question
            )
            if st.session_state.get("ma_question_input", "") == prev_question:
                st.session_state["ma_question_input"] = active_preset.question

        research_question = st.text_area(
            t("research.consensus.question_label"),
            value=active_preset.question,
            height=90,
            key="ma_question_input",
        )

        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            run_consensus_btn = st.button(
                t("research.consensus.run_button"), type="primary", width="stretch"
            )
        with col_info:
            active_subagents = []
            if params["enable_evidence"]:
                active_subagents.append(t("sidebar.evidence_specialist_label"))
            if params["enable_guideline"]:
                active_subagents.append(t("sidebar.guideline_specialist_label"))
            pipeline_text = " + ".join(active_subagents) or t("research.consensus.none")
            st.caption(t("research.consensus.active_pipeline", pipeline=pipeline_text))

        if run_consensus_btn:
            with st.status(t("research.consensus.status_executing"), expanded=True) as status:
                st.write(t("research.consensus.status_step1"))
                st.write(t("research.consensus.status_step2"))
                st.write(t("research.consensus.status_step3"))
                agent_req = MultiAgentConsensusRequest(
                    question=apply_language_directive(research_question, current_locale),
                    model=params["model_id"],
                    enable_evidence_agent=params["enable_evidence"],
                    enable_guideline_agent=params["enable_guideline"],
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                agent_resp = run_multiagent(agent_req)
                status.update(
                    label=t("research.consensus.status_complete"),
                    state="complete",
                    expanded=False,
                )

            st.divider()

            # Executive Summary First: Immediate Clinical Bottom Line
            st.markdown(t("research.consensus.brief_title"))
            st.markdown(agent_resp.final_synthesis)
            st.caption(f"ℹ️ {agent_resp.safety_disclaimer}")

            st.divider()

            # Structured Drill-Down Tabs
            res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs(
                [
                    t("research.consensus.tabs.specialist"),
                    t("research.consensus.tabs.consensus"),
                    t("research.consensus.tabs.picot"),
                    t("research.consensus.tabs.timeline"),
                ]
            )

            with res_tab1:
                render_evidence_vs_guidelines(
                    agent_resp.evidence_findings,
                    agent_resp.guideline_findings,
                )

            with res_tab2:
                render_consensus_matrix(agent_resp.consensus_matrix)

            with res_tab3:
                st.markdown(t("research.consensus.picot_scope_title"))
                p_cols = st.columns(4)
                with p_cols[0]:
                    st.markdown(
                        f"{t('research.consensus.population')}\n\n{agent_resp.normalized_picot.get('population', '')}"
                    )
                with p_cols[1]:
                    st.markdown(
                        f"{t('research.consensus.intervention')}\n\n{agent_resp.normalized_picot.get('intervention', '')}"
                    )
                with p_cols[2]:
                    st.markdown(
                        f"{t('research.consensus.comparator')}\n\n{agent_resp.normalized_picot.get('comparator', '')}"
                    )
                with p_cols[3]:
                    st.markdown(
                        f"{t('research.consensus.outcomes')}\n\n{', '.join(agent_resp.normalized_picot.get('outcomes', []))}"
                    )

                if agent_resp.sources:
                    st.markdown(t("research.consensus.verified_citations"))
                    for src in agent_resp.sources:
                        st.markdown(
                            f"- [{src.get('title')}]({src.get('url')}) `({src.get('type')})`"
                        )

            with res_tab4:
                render_execution_timeline(agent_resp.execution_steps)

    # 2. Benchmark Audit Mode
    elif research_mode == "benchmark_audit":
        st.subheader(t("research.benchmark.subheader"))
        st.markdown(t("research.benchmark.description"))

        preset_map = {p.id: p for p in preset_questions}
        case_choices = list(preset_map.keys())

        def format_case_choice(cid: str) -> str:
            raw_case = preset_map.get(cid)
            if not raw_case:
                return cid
            loc_case = get_localized_preset_inquiry(raw_case, current_locale)
            return f"[{loc_case.id}] {loc_case.title} ({loc_case.category})"

        c_sel1, c_sel2 = st.columns([2, 1])
        with c_sel1:
            selected_case_id = st.selectbox(
                t("research.benchmark.select_label"),
                options=case_choices,
                format_func=format_case_choice,
                key="bench_case_select",
            )
        with c_sel2:
            st.caption(t("research.benchmark.category_label"))
            raw_bench_case = preset_map[selected_case_id]
            active_bench_case = get_localized_preset_inquiry(raw_bench_case, current_locale)
            st.markdown(f"**{get_case_type_badge(raw_bench_case.case_type)}**")

        with st.expander(t("research.benchmark.expander_title"), expanded=True):
            p_c1, p_c2, p_c3 = st.columns(3)
            with p_c1:
                st.info(f"{t('research.benchmark.lesson_title')}\n\n{active_bench_case.pedagogical_lesson}")
            with p_c2:
                st.error(f"{t('research.benchmark.flaw_title')}\n\n{active_bench_case.expected_without_agent_flaw}")
            with p_c3:
                st.success(f"{t('research.benchmark.benefit_title')}\n\n{active_bench_case.expected_with_agent_benefit}")

        prev_bench_id = st.session_state.get("_last_bench_preset_id", selected_case_id)
        if selected_case_id != prev_bench_id:
            st.session_state["bench_question_input"] = active_bench_case.question
            st.session_state["_last_bench_preset_id"] = selected_case_id
        elif current_locale != prev_locale:
            prev_b_question = get_preset_question_for_locale(
                selected_case_id, prev_locale, raw_bench_case.question
            )
            if st.session_state.get("bench_question_input", "") == prev_b_question:
                st.session_state["bench_question_input"] = active_bench_case.question

        bench_question = st.text_area(
            t("research.benchmark.scenario_label"),
            value=active_bench_case.question,
            height=90,
            key="bench_question_input",
        )

        col_bench_btn, col_bench_meta = st.columns([1, 2])
        with col_bench_btn:
            run_compare_btn = st.button(
                t("research.benchmark.run_button"),
                type="primary",
                width="stretch",
                key="btn_run_compare",
            )
        with col_bench_meta:
            st.caption(
                t(
                    "research.benchmark.comparing_caption",
                    model=params["model_info"].display_name,
                )
            )

        if run_compare_btn:
            with st.status(
                t("research.benchmark.status_running", title=active_bench_case.title),
                expanded=True,
            ) as status:
                st.write(t("research.benchmark.status_step1"))
                st.write(t("research.benchmark.status_step2"))
                st.write(t("research.benchmark.status_step3"))
                comp_req = ComparativeAnalysisRequest(
                    question=apply_language_directive(bench_question, current_locale),
                    case_id=selected_case_id,
                    model=params["model_id"],
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                comp_res = run_comparative_analysis(comp_req)
                status.update(
                    label=t("research.benchmark.status_complete"),
                    state="complete",
                    expanded=False,
                )

            st.divider()

            # Pedagogical takeaway alert banner
            takeaway = (
                active_bench_case.pedagogical_lesson
                if current_locale == "tr" and comp_res.case_id == selected_case_id
                else comp_res.pedagogical_takeaway
            )
            st.info(t("research.benchmark.conclusion_banner", takeaway=takeaway))

            # Side-by-side view
            render_direct_vs_agent_side_by_side(comp_res.without_agent, comp_res.with_agent)

            st.divider()

            # Sub-tabs for deep inspection
            b_tab1, b_tab2, b_tab3, b_tab4 = st.tabs(
                [
                    t("research.benchmark.tabs.scorecard"),
                    t("research.benchmark.tabs.matrix"),
                    t("research.benchmark.tabs.breakdown"),
                    t("research.benchmark.tabs.raw_json"),
                ]
            )

            with b_tab1:
                render_comparative_scorecard(comp_res.scorecard)

            with b_tab2:
                render_consensus_matrix(comp_res.with_agent.consensus_matrix)

            with b_tab3:
                render_execution_timeline(comp_res.with_agent.execution_steps)

            with b_tab4:
                st.json(comp_res.model_dump())

    # 3. PICOT Query Decomposer Mode
    elif research_mode == "picot_decomposer":
        st.subheader(t("research.picot.subheader"))
        st.caption(t("research.picot.caption"))

        default_picot_val = (
            "Obez yetişkinlerde ventral ve insizyonel fıtıklar için robotik ve laparoskopik "
            "greft onarımı cerrahi alan olayları ve işe dönüş açısından güncel kanıtlar ne söylemektedir?"
            if current_locale == "tr"
            else (
                "What does recent evidence say about robotic vs laparoscopic mesh repair for ventral "
                "and incisional hernias in obese adults regarding surgical site occurrences and return to work?"
            )
        )

        decom_input = st.text_area(
            t("research.picot.input_label"),
            value=default_picot_val,
            height=90,
            key="picot_decomp_input",
        )

        if st.button(t("research.picot.run_button"), type="primary"):
            with st.spinner(t("research.picot.spinner")):
                decomp_res = local_service.decompose_picot(
                    PICOTDecomposeRequest(
                        question=decom_input, model=params["model_id"], mock_mode=True
                    )
                )

            c1, c2 = st.columns(2)
            with c1:
                st.info(f"{t('research.picot.population')}\n{decomp_res.population}")
                st.success(f"{t('research.picot.intervention')}\n{decomp_res.intervention}")
                st.warning(f"{t('research.picot.comparator')}\n{decomp_res.comparator}")
            with c2:
                st.info(f"{t('research.picot.outcomes')}\n" + "\n".join([f"- {o}" for o in decomp_res.outcomes]))
                st.caption(t("research.picot.timeline", time_range=decomp_res.time_range))
                st.markdown(
                    f"{t('research.picot.keywords')} "
                    + " ".join([f"`{k}`" for k in decomp_res.search_keywords])
                )

    # 4. Specialist Deep-Dive Mode
    elif research_mode == "specialist_deep_dive":
        st.subheader(t("research.specialist.subheader"))
        st.caption(t("research.specialist.caption"))

        spec_mode = st.segmented_control(
            t("research.specialist.target_label"),
            ["evidence", "guideline"],
            format_func=lambda s: t(f"research.specialist.{s}"),
            default="evidence",
        )

        default_spec_q = (
            "Elektif kolorektal cerrahide prehabilitasyon"
            if current_locale == "tr"
            else "Prehabilitation in elective colorectal surgery"
        )
        spec_query = st.text_input(
            t("research.specialist.query_label"),
            value=default_spec_q,
            key="spec_query_input",
        )

        if st.button(t("research.specialist.run_button"), type="primary"):
            with st.spinner(t("research.specialist.spinner")):
                is_evid = spec_mode == "evidence"
                req = MultiAgentConsensusRequest(
                    question=apply_language_directive(spec_query, current_locale),
                    model=params["model_id"],
                    enable_evidence_agent=is_evid,
                    enable_guideline_agent=not is_evid,
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                spec_resp = run_multiagent(req)

            if is_evid:
                st.markdown(spec_resp.evidence_findings.get("summary", t("research.specialist.no_findings")))
                for s in spec_resp.evidence_findings.get("key_study_findings", []):
                    st.markdown(
                        f"- **[{s.get('study_title')}]({s.get('url')})** — *{s.get('evidence_type')}* ({s.get('year')})"
                    )
            else:
                st.markdown(spec_resp.guideline_findings.get("summary", t("research.specialist.no_findings")))
                for g in spec_resp.guideline_findings.get("guideline_statements", []):
                    st.markdown(
                        f"- **[{g.get('organization')} — {g.get('guideline_title')}]({g.get('url')})** ({g.get('year')})"
                    )


# -----------------------------------------------------------------------------
# TAB 2: Multimodal Vision & Video Studio
# -----------------------------------------------------------------------------
with tab_multimodal:
    st.subheader(t("multimodal.subheader"))
    st.caption(t("multimodal.caption"))

    media_mode = st.segmented_control(
        "Multimodal Inspection Mode:",
        options=["static_vision", "dynamic_video"],
        format_func=lambda m: t(f"multimodal.modes.{m}"),
        default="static_vision",
        label_visibility="collapsed",
    )

    if media_mode == "static_vision":
        vis_left, vis_right = st.columns([1, 1])

        with vis_left:
            st.markdown(t("multimodal.step1_image"))
            image_source = st.segmented_control(
                "Select Image Source:",
                ["preset", "upload"],
                format_func=lambda s: t(f"multimodal.image_sources.{s}"),
                default="preset",
                key="vis_img_source",
            )

            image_bytes: Optional[bytes] = None
            image_filename = "radiograph.jpeg"
            image_mime = "image/jpeg"
            active_preset_id: Optional[str] = None
            preset_obj: Optional[Any] = None
            raw_preset_obj: Optional[Any] = None

            if image_source == "preset":
                preset_options = [p.id for p in preset_images]

                def format_preset_img(pid: str) -> str:
                    raw_p = next(p for p in preset_images if p.id == pid)
                    loc_p = get_localized_preset_image(raw_p, current_locale)
                    return f"{loc_p.title} ({loc_p.filename})"

                selected_preset_id = st.selectbox(
                    t("multimodal.choose_preset_image"),
                    options=preset_options,
                    format_func=format_preset_img,
                    key="vis_preset_select",
                )
                image_bytes = local_service.get_preset_image_bytes(selected_preset_id)
                raw_preset_obj = next(p for p in preset_images if p.id == selected_preset_id)
                preset_obj = get_localized_preset_image(raw_preset_obj, current_locale)
                active_preset_id = selected_preset_id
                image_filename = preset_obj.filename
                guessed_mime, _ = mimetypes.guess_type(preset_obj.filename)
                image_mime = guessed_mime or "image/jpeg"
                st.caption(f"📝 {preset_obj.description}")
            else:
                uploaded_file = st.file_uploader(
                    t("multimodal.upload_image_label"),
                    type=["png", "jpg", "jpeg", "webp"],
                    key="vis_file_uploader",
                )
                if uploaded_file is not None:
                    image_bytes = uploaded_file.getvalue()
                    image_filename = uploaded_file.name
                    image_mime = uploaded_file.type or "image/jpeg"

            if image_bytes:
                pil_img = Image.open(io.BytesIO(image_bytes))
                st.image(
                    pil_img,
                    caption=t(
                        "multimodal.visual_input_caption",
                        filename=image_filename,
                        w=pil_img.width,
                        h=pil_img.height,
                        kb=len(image_bytes) / 1024,
                    ),
                    width="stretch",
                )

        with vis_right:
            st.markdown(t("multimodal.step2_image"))

            # Dynamic prompts based on selected preset image
            if preset_obj and getattr(preset_obj, "suggested_prompts", None):
                quick_prompts = list(preset_obj.suggested_prompts) + [t("multimodal.custom_prompt_option")]
            else:
                quick_prompts = [
                    (
                        "Bu görüntüde yalnızca gözlemlenebilir görsel anatomik ve radyolojik özellikleri tanımlayın."
                        if current_locale == "tr"
                        else "Describe only the observable visual anatomical and radiological features in this image."
                    ),
                    (
                        "Görünür temel bulguları, sınırları, dizilimi ve teknik hususları ayrıntılandırın."
                        if current_locale == "tr"
                        else "Detail the key findings, margins, alignment, and technical aspects visible."
                    ),
                    t("multimodal.custom_prompt_option"),
                ]

            selected_prompt_template = st.selectbox(
                t("multimodal.quick_prompts_image"),
                options=quick_prompts,
                index=0,
                key="vis_prompt_select",
            )

            if selected_prompt_template == t("multimodal.custom_prompt_option"):
                default_prompt_text = (
                    "Hangi anatomik yapılar ve radyolojik bulgular görünmektedir?"
                    if current_locale == "tr"
                    else "What anatomical structures and radiological findings are visible?"
                )
            else:
                default_prompt_text = selected_prompt_template

            prev_vis_id = st.session_state.get("_last_vis_preset_id", active_preset_id)
            if active_preset_id != prev_vis_id:
                st.session_state["vis_user_prompt"] = default_prompt_text
                st.session_state["_last_vis_preset_id"] = active_preset_id
            elif current_locale != prev_locale and raw_preset_obj:
                prev_prompts = get_localized_preset_image(raw_preset_obj, prev_locale).suggested_prompts
                curr_val = st.session_state.get("vis_user_prompt", "")
                if curr_val in prev_prompts and preset_obj and preset_obj.suggested_prompts:
                    idx = prev_prompts.index(curr_val)
                    if idx < len(preset_obj.suggested_prompts):
                        st.session_state["vis_user_prompt"] = preset_obj.suggested_prompts[idx]

            user_prompt = st.text_area(
                t("multimodal.inquiry_prompt_label"),
                value=default_prompt_text,
                height=130,
                key="vis_user_prompt",
            )

            st.caption(t("multimodal.safety_image"))

            run_multimodal_btn = st.button(
                t("multimodal.run_image_button"), type="primary", width="stretch"
            )

        if run_multimodal_btn:
            if not image_bytes:
                st.error(t("multimodal.error_no_image"))
            else:
                with st.spinner(
                    t("multimodal.spinner_image", model=params["model_info"].display_name)
                ):
                    req = MultimodalInquiryRequest(
                        prompt=apply_language_directive(user_prompt, current_locale),
                        image_base64=base64.b64encode(image_bytes).decode("utf-8"),
                        image_mime_type=image_mime,
                        preset_image_id=active_preset_id,
                        model=params["model_id"],
                        temperature=params["temperature"],
                        top_p=params["top_p"],
                        max_output_tokens=params["max_output_tokens"],
                        thinking_budget=params["thinking_budget"],
                        thinking_level=params["thinking_level"],
                        mock_mode=params["mock_mode"],
                    )
                    vis_resp = run_multimodal(req)

                st.divider()
                resp_tab1, resp_tab2, resp_tab3 = st.tabs(
                    [
                        t("multimodal.tabs.observation"),
                        t("multimodal.tabs.parameters"),
                        t("multimodal.tabs.payload"),
                    ]
                )

                with resp_tab1:
                    st.markdown(vis_resp.text)
                    if vis_resp.visual_elements_detected:
                        st.markdown(t("multimodal.detected_features"))
                        st.write(", ".join([f"`{el}`" for el in vis_resp.visual_elements_detected]))
                    st.caption(
                        t("multimodal.latency_caption", ms=vis_resp.latency_ms, model=vis_resp.model)
                    )

                with resp_tab2:
                    st.markdown(
                        f"""
                        {t("multimodal.param_model_id", model=vis_resp.model)}
                        {t("multimodal.param_latency", ms=vis_resp.latency_ms)}
                        {t("multimodal.param_tokens", tokens=vis_resp.token_estimate)}
                        {t("multimodal.param_thinking_level", level=params.get("thinking_level") or "N/A")}
                        {t("multimodal.param_thinking_budget", budget=params.get("thinking_budget") if params.get("thinking_budget") is not None else "N/A")}
                        {t("multimodal.param_temperature", temp=params["temperature"])}
                        {t("multimodal.param_top_p", top_p=params["top_p"])}
                        {t("multimodal.param_max_tokens", max_tokens=params["max_output_tokens"])}
                        """
                    )
                    st.code(user_prompt, language="markdown")

                with resp_tab3:
                    st.json(vis_resp.model_dump())

    elif media_mode == "dynamic_video":
        vid_left, vid_right = st.columns([1, 1])

        with vid_left:
            st.markdown(t("multimodal.step1_video"))
            video_source = st.segmented_control(
                "Select Video Source:",
                ["preset", "upload"],
                format_func=lambda s: t(f"multimodal.video_sources.{s}"),
                default="preset",
                key="vid_source_radio",
            )

            video_bytes: Optional[bytes] = None
            video_filename = "apical_4_chamber_echo.mp4"
            video_mime = "video/mp4"
            active_video_id: Optional[str] = None
            preset_vid_obj: Optional[Any] = None
            raw_vid_obj: Optional[Any] = None

            if video_source == "preset":
                preset_vid_options = [v.id for v in preset_videos]

                def format_preset_vid(vid: str) -> str:
                    raw_v = next(v for v in preset_videos if v.id == vid)
                    loc_v = get_localized_preset_video(raw_v, current_locale)
                    return f"{loc_v.title} ({loc_v.filename})"

                selected_vid_id = st.selectbox(
                    t("multimodal.choose_preset_video"),
                    options=preset_vid_options,
                    format_func=format_preset_vid,
                    key="vid_preset_select",
                )
                video_bytes = local_service.get_preset_video_bytes(selected_vid_id)
                raw_vid_obj = next(v for v in preset_videos if v.id == selected_vid_id)
                preset_vid_obj = get_localized_preset_video(raw_vid_obj, current_locale)
                active_video_id = selected_vid_id
                video_filename = preset_vid_obj.filename
                guessed_mime, _ = mimetypes.guess_type(preset_vid_obj.filename)
                video_mime = guessed_mime or "video/mp4"
                st.caption(f"📝 {preset_vid_obj.description}")
            else:
                uploaded_vid = st.file_uploader(
                    t("multimodal.upload_video_label"),
                    type=["mp4", "webm", "mov"],
                    key="vid_file_uploader",
                )
                if uploaded_vid is not None:
                    video_bytes = uploaded_vid.getvalue()
                    video_filename = uploaded_vid.name
                    video_mime = uploaded_vid.type or "video/mp4"

            if video_bytes:
                st.video(video_bytes, format=video_mime, autoplay=True, loop=True, muted=True)
                st.caption(
                    t(
                        "multimodal.video_clip_caption",
                        filename=video_filename,
                        kb=len(video_bytes) / 1024,
                        mime=video_mime,
                    )
                )

        with vid_right:
            st.markdown(t("multimodal.step2_video"))

            if preset_vid_obj and getattr(preset_vid_obj, "suggested_prompts", None):
                quick_vid_prompts = list(preset_vid_obj.suggested_prompts) + [
                    t("multimodal.custom_prompt_option")
                ]
            else:
                quick_vid_prompts = [
                    (
                        "Bu ekokardiyogram video klibinde gözlemlenebilir kardiyak yapıları ve dinamik duvar hareketini tanımlayın."
                        if current_locale == "tr"
                        else "Describe the observable cardiac structures and dynamic wall motion in this echocardiogram video clip."
                    ),
                    (
                        "Kardiyak döngü boyunca sol ventrikül ile sağ ventrikülün kasılmasını ve simetrisini değerlendirin."
                        if current_locale == "tr"
                        else "Evaluate the contraction and symmetry of the left ventricle vs right ventricle across the cardiac cycle."
                    ),
                    t("multimodal.custom_prompt_option"),
                ]

            selected_vid_prompt = st.selectbox(
                t("multimodal.quick_prompts_video"),
                options=quick_vid_prompts,
                index=0,
                key="vid_prompt_select",
            )

            if selected_vid_prompt == t("multimodal.custom_prompt_option"):
                default_vid_text = (
                    "Bu klipte hangi dinamik anatomik hareketler ve duvar hareketi paternleri gözlemlenebilir?"
                    if current_locale == "tr"
                    else "What dynamic anatomical movements and wall motion patterns are observable in this clip?"
                )
            else:
                default_vid_text = selected_vid_prompt

            prev_vid_id = st.session_state.get("_last_vid_preset_id", active_video_id)
            if active_video_id != prev_vid_id:
                st.session_state["vid_user_prompt"] = default_vid_text
                st.session_state["_last_vid_preset_id"] = active_video_id
            elif current_locale != prev_locale and raw_vid_obj:
                prev_prompts = get_localized_preset_video(raw_vid_obj, prev_locale).suggested_prompts
                curr_val = st.session_state.get("vid_user_prompt", "")
                if curr_val in prev_prompts and preset_vid_obj and preset_vid_obj.suggested_prompts:
                    idx = prev_prompts.index(curr_val)
                    if idx < len(preset_vid_obj.suggested_prompts):
                        st.session_state["vid_user_prompt"] = preset_vid_obj.suggested_prompts[idx]

            user_vid_prompt = st.text_area(
                t("multimodal.temporal_prompt_label"),
                value=default_vid_text,
                height=130,
                key="vid_user_prompt",
            )

            st.caption(t("multimodal.safety_video"))

            run_video_btn = st.button(
                t("multimodal.run_video_button"),
                type="primary",
                width="stretch",
                key="run_video_btn",
            )

        if run_video_btn:
            if not video_bytes:
                st.error(t("multimodal.error_no_video"))
            else:
                with st.spinner(
                    t("multimodal.spinner_video", model=params["model_info"].display_name)
                ):
                    req = MultimodalInquiryRequest(
                        prompt=apply_language_directive(user_vid_prompt, current_locale),
                        video_base64=base64.b64encode(video_bytes).decode("utf-8"),
                        video_mime_type=video_mime,
                        preset_video_id=active_video_id,
                        model=params["model_id"],
                        temperature=params["temperature"],
                        top_p=params["top_p"],
                        max_output_tokens=params["max_output_tokens"],
                        thinking_budget=params["thinking_budget"],
                        thinking_level=params["thinking_level"],
                        mock_mode=params["mock_mode"],
                    )
                    vid_resp = run_multimodal(req)

                st.divider()
                v_tab1, v_tab2, v_tab3 = st.tabs(
                    [
                        t("multimodal.tabs.temporal_observation"),
                        t("multimodal.tabs.parameters"),
                        t("multimodal.tabs.payload"),
                    ]
                )

                with v_tab1:
                    st.markdown(vid_resp.text)
                    if vid_resp.visual_elements_detected:
                        st.markdown(t("multimodal.detected_structures"))
                        st.write(", ".join([f"`{el}`" for el in vid_resp.visual_elements_detected]))
                    st.caption(
                        t("multimodal.latency_caption", ms=vid_resp.latency_ms, model=vid_resp.model)
                    )

                with v_tab2:
                    st.markdown(
                        f"""
                        {t("multimodal.param_model_id", model=vid_resp.model)}
                        {t("multimodal.param_latency", ms=vid_resp.latency_ms)}
                        {t("multimodal.param_tokens", tokens=vid_resp.token_estimate)}
                        {t("multimodal.param_thinking_level", level=params.get("thinking_level") or "N/A")}
                        {t("multimodal.param_thinking_budget", budget=params.get("thinking_budget") if params.get("thinking_budget") is not None else "N/A")}
                        {t("multimodal.param_temperature", temp=params["temperature"])}
                        {t("multimodal.param_top_p", top_p=params["top_p"])}
                        {t("multimodal.param_max_tokens", max_tokens=params["max_output_tokens"])}
                        """
                    )
                    st.code(user_vid_prompt, language="markdown")

                with v_tab3:
                    st.json(vid_resp.model_dump())


# -----------------------------------------------------------------------------
# TAB 3: API & Diagnostics
# -----------------------------------------------------------------------------
with tab_diagnostics:
    st.subheader(t("diagnostics.subheader"))

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown(t("diagnostics.rest_title"))
        try:
            with httpx.Client(timeout=3.0) as client:
                res = client.get(f"{params['fastapi_url']}/api/health")
                if res.status_code == 200:
                    st.success(t("diagnostics.rest_online"))
                    st.json(res.json())
                else:
                    st.warning(t("diagnostics.rest_status", status=res.status_code))
        except Exception as ex:
            st.error(t("diagnostics.rest_offline", url=params["fastapi_url"], ex=ex))
            st.caption(t("diagnostics.rest_run_help"))

    with d_col2:
        st.markdown(t("diagnostics.tips_title"))
        st.info(t("diagnostics.tips_body"))

        st.markdown(t("diagnostics.env_title"))
        has_key = bool(os.environ.get("GOOGLE_API_KEY"))
        has_proj = bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))
        st.write(f"- `GOOGLE_API_KEY`: {t('diagnostics.configured') if has_key else t('diagnostics.not_set')}")
        st.write(
            f"- `GOOGLE_CLOUD_PROJECT`: {t('diagnostics.configured') if has_proj else t('diagnostics.not_set')}"
        )
        st.write(t("diagnostics.active_model", model=params["model_id"]))

# Record locale at the end of execution to track subsequent transitions
st.session_state["_last_locale"] = current_locale
