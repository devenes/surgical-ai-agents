"""Streamlit Main Application for Surgical AI Studio (FastAPI + Streamlit).

Supports multimodal image understanding and a 2-subagent (Evidence & Guideline)
orchestration pipeline with token-optimized offline mode and interactive tabs.
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

# Page configuration
st.set_page_config(
    page_title="Surgical AI Studio | Multimodal & Multi-Agent",
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

# Sidebar Controls
params = render_sidebar_controls(models)


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
            st.warning(f"⚠️ FastAPI REST request failed ({e}). Falling back to in-process service.")
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
            st.warning(f"⚠️ FastAPI REST request failed ({e}). Falling back to in-process service.")
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
            st.warning(f"⚠️ FastAPI REST request failed ({e}). Falling back to in-process service.")
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
            st.warning(f"⚠️ FastAPI REST request failed ({e}). Falling back to in-process service.")
    return local_service.execute_monolithic_direct(req)


# =============================================================================
# Main Header
# =============================================================================
st.header("🩺 Surgical AI Studio: Multimodal & Multi-Agent Research", divider="rainbow")
mode_text = "⚡ Zero-Token Offline" if params["mock_mode"] else "🌐 Live Vertex AI"
agents_count = int(params["enable_evidence"]) + int(params["enable_guideline"])
thinking_desc = params.get("thinking_level") or (
    f"{params['thinking_budget']} tokens" if params.get("thinking_budget") is not None else "Default"
)
st.caption(
    f"🧠 **Model:** `{params['model_info'].display_name}` &nbsp;•&nbsp; "
    f"💭 **Thinking:** `{thinking_desc}` &nbsp;•&nbsp; "
    f"🔌 **Mode:** `{mode_text}` &nbsp;•&nbsp; "
    f"🤖 **Sub-Agents:** `{agents_count} Active` &nbsp;•&nbsp; "
    f"⚙️ **Backend:** `{params['connection_mode']}`"
)


# =============================================================================
# Application Tabs
# =============================================================================
tab_research, tab_multimodal, tab_diagnostics = st.tabs(
    [
        "🔬 Clinical Research & Consensus",
        "🖼️ Multimodal Vision & Video",
        "⚙️ API & Diagnostics",
    ]
)


# -----------------------------------------------------------------------------
# TAB 1: Clinical Research & Consensus
# -----------------------------------------------------------------------------
with tab_research:
    research_mode = st.segmented_control(
        "Research Workflow:",
        options=[
            "🤖 Multi-Agent Consensus",
            "⚖️ Benchmark Audit (With vs. Without Agents)",
            "⚡ PICOT Query Decomposer",
            "📚 Specialist Deep-Dive",
        ],
        default="🤖 Multi-Agent Consensus",
        label_visibility="collapsed",
    )

    # 1. Primary Multi-Agent Consensus Mode
    if research_mode == "🤖 Multi-Agent Consensus":
        st.subheader("🤖 Multi-Agent Consensus Architecture")
        st.caption(
            "Orchestrates a **Coordinator Agent** delegating research in parallel to two specialized sub-agents:\n"
            "• **Evidence Specialist:** Peer-reviewed randomized trials (PubMed)\n"
            "• **Guideline Specialist:** Clinical practice guidelines from major surgical societies (ASCRS, ERAS, SAGES)\n"
            "• **Coordinator Synthesis:** Normalizes into PICOT, reconciles agreements/divergences, and generates consensus matrix."
        )

        preset_titles = {p.id: f"{p.title} ({p.category})" for p in preset_questions}
        selected_preset_qid = st.selectbox(
            "Choose Preset Surgical Topic or Customize Below:",
            options=list(preset_titles.keys()),
            format_func=lambda x: preset_titles[x],
            key="ma_preset_select",
        )

        active_preset = next(p for p in preset_questions if p.id == selected_preset_qid)
        st.caption(
            f"{get_case_type_badge(active_preset.case_type)} — *{active_preset.pedagogical_lesson}*"
        )

        research_question = st.text_area(
            "Clinical Research Question:",
            value=active_preset.question,
            height=90,
            key="ma_question_input",
        )

        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            run_consensus_btn = st.button(
                "🚀 Execute Multi-Agent Consensus", type="primary", width="stretch"
            )
        with col_info:
            active_subagents = []
            if params["enable_evidence"]:
                active_subagents.append("📚 Evidence Specialist")
            if params["enable_guideline"]:
                active_subagents.append("📋 Guideline Specialist")
            st.caption(f"Active Pipeline: Coordinator ➔ {' + '.join(active_subagents) or 'None'}")

        if run_consensus_btn:
            with st.status("Executing multi-agent research workflow...", expanded=True) as status:
                st.write("1. Normalizing inquiry into clinical PICOT framework...")
                st.write("2. Querying Evidence & Guideline specialists in parallel...")
                st.write("3. Reconciling findings into consensus brief and discrepancy matrix...")
                agent_req = MultiAgentConsensusRequest(
                    question=research_question,
                    model=params["model_id"],
                    enable_evidence_agent=params["enable_evidence"],
                    enable_guideline_agent=params["enable_guideline"],
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                agent_resp = run_multiagent(agent_req)
                status.update(
                    label="Multi-Agent Consensus brief generated!",
                    state="complete",
                    expanded=False,
                )

            st.divider()

            # Executive Summary First: Immediate Clinical Bottom Line
            st.markdown("### 📝 Master Evidence Brief")
            st.markdown(agent_resp.final_synthesis)
            st.caption(f"ℹ️ {agent_resp.safety_disclaimer}")

            st.divider()

            # Structured Drill-Down Tabs
            res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs(
                [
                    "📑 Specialist Findings (Side-by-Side)",
                    "⚖️ Consensus & Discrepancies",
                    "📌 Normalized PICOT & Citations",
                    "⏱️ Execution Pipeline Trace",
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
                st.markdown("#### 📌 Normalized PICOT Scope")
                p_cols = st.columns(4)
                with p_cols[0]:
                    st.markdown(
                        f"**Population:**\n\n{agent_resp.normalized_picot.get('population', '')}"
                    )
                with p_cols[1]:
                    st.markdown(
                        f"**Intervention:**\n\n{agent_resp.normalized_picot.get('intervention', '')}"
                    )
                with p_cols[2]:
                    st.markdown(
                        f"**Comparator:**\n\n{agent_resp.normalized_picot.get('comparator', '')}"
                    )
                with p_cols[3]:
                    st.markdown(
                        f"**Outcomes:**\n\n{', '.join(agent_resp.normalized_picot.get('outcomes', []))}"
                    )

                if agent_resp.sources:
                    st.markdown("#### 🔗 Verified Citations")
                    for src in agent_resp.sources:
                        st.markdown(
                            f"- [{src.get('title')}]({src.get('url')}) `({src.get('type')})`"
                        )

            with res_tab4:
                render_execution_timeline(agent_resp.execution_steps)

    # 2. Benchmark Audit Mode
    elif research_mode == "⚖️ Benchmark Audit (With vs. Without Agents)":
        st.subheader("⚖️ Empirical Benchmark: Monolithic Baseline vs. 2-Subagent Architecture")
        st.markdown(
            "Demonstrates why multi-agent specialization is essential for high-stakes surgical inquiries. "
            "Direct zero-shot monolithic models frequently **hallucinate citations**, **conflate trials with guidelines**, "
            "and **fail safety boundaries** by dispensing direct, unverified patient advice. "
            "The **2-Subagent Architecture** grounds inquiries in verifiable PubMed RCTs and surgical society guidelines "
            "while enforcing an automatic educational refusal gate."
        )

        preset_map = {p.id: p for p in preset_questions}
        case_choices = list(preset_map.keys())

        def format_case_choice(cid: str) -> str:
            case = preset_map.get(cid)
            if not case:
                return cid
            return f"[{case.id}] {case.title} ({case.category})"

        c_sel1, c_sel2 = st.columns([2, 1])
        with c_sel1:
            selected_case_id = st.selectbox(
                "Select Clinical Benchmark Case:",
                options=case_choices,
                format_func=format_case_choice,
                key="bench_case_select",
            )
        with c_sel2:
            st.caption("Benchmark Category:")
            active_bench_case = preset_map[selected_case_id]
            st.markdown(f"**{get_case_type_badge(active_bench_case.case_type)}**")

        with st.expander("💡 Case Pedagogical Context & Expected Flaws", expanded=True):
            p_c1, p_c2, p_c3 = st.columns(3)
            with p_c1:
                st.info(f"💡 **Pedagogical Lesson**\n\n{active_bench_case.pedagogical_lesson}")
            with p_c2:
                st.error(
                    f"❌ **Expected Monolithic Flaw**\n\n{active_bench_case.expected_without_agent_flaw}"
                )
            with p_c3:
                st.success(
                    f"🛡️ **Multi-Agent Benefit**\n\n{active_bench_case.expected_with_agent_benefit}"
                )

        bench_question = st.text_area(
            "Clinical Research / Scenario Prompt:",
            value=active_bench_case.question,
            height=90,
            key="bench_question_input",
        )

        col_bench_btn, col_bench_meta = st.columns([1, 2])
        with col_bench_btn:
            run_compare_btn = st.button(
                "🚀 Run Head-to-Head Comparison",
                type="primary",
                width="stretch",
                key="btn_run_compare",
            )
        with col_bench_meta:
            st.caption(
                f"Comparing: **Monolithic Baseline ({params['model_info'].display_name})** vs. "
                f"**Coordinator + Evidence & Guideline Specialists**"
            )

        if run_compare_btn:
            with st.status(
                f"Running head-to-head evaluation on '{active_bench_case.title}'...",
                expanded=True,
            ) as status:
                st.write("1. Querying monolithic baseline model (zero-shot)...")
                st.write("2. Orchestrating 2-subagent consensus pipeline...")
                st.write("3. Scoring across 5 clinical reliability dimensions...")
                comp_req = ComparativeAnalysisRequest(
                    question=bench_question,
                    case_id=selected_case_id,
                    model=params["model_id"],
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                comp_res = run_comparative_analysis(comp_req)
                status.update(
                    label="Head-to-head benchmark complete!",
                    state="complete",
                    expanded=False,
                )

            st.divider()

            # Pedagogical takeaway alert banner
            st.info(f"🎯 **Audit Conclusion:** {comp_res.pedagogical_takeaway}")

            # Side-by-side view
            render_direct_vs_agent_side_by_side(comp_res.without_agent, comp_res.with_agent)

            st.divider()

            # Sub-tabs for deep inspection
            b_tab1, b_tab2, b_tab3, b_tab4 = st.tabs(
                [
                    "📊 5-Dimension Audit Scorecard",
                    "⚖️ Reconciled Consensus Matrix",
                    "⏱️ Execution Pipeline Breakdown",
                    "📦 Full Raw Benchmark JSON",
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
    elif research_mode == "⚡ PICOT Query Decomposer":
        st.subheader("⚡ PICOT Query Decomposer (Sub-Agent 1 Utility)")
        st.caption(
            "Deconstructs complex, ambiguous clinical questions into standardized epidemiological "
            "**PICOT** (Population, Intervention, Comparator, Outcomes, Timeline) search vectors."
        )

        decom_input = st.text_area(
            "Enter raw surgical inquiry:",
            value=(
                "What does recent evidence say about robotic vs laparoscopic mesh repair for ventral "
                "and incisional hernias in obese adults regarding surgical site occurrences and return to work?"
            ),
            height=90,
            key="picot_decomp_input",
        )

        if st.button("🧩 Decompose Inquiry", type="primary"):
            with st.spinner("Extracting PICOT parameters..."):
                decomp_res = local_service.decompose_picot(
                    PICOTDecomposeRequest(
                        question=decom_input, model=params["model_id"], mock_mode=True
                    )
                )

            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**👥 Population:**\n{decomp_res.population}")
                st.success(f"**💉 Intervention:**\n{decomp_res.intervention}")
                st.warning(f"**⚖️ Comparator:**\n{decomp_res.comparator}")
            with c2:
                st.info("**🎯 Outcomes:**\n" + "\n".join([f"- {o}" for o in decomp_res.outcomes]))
                st.caption(f"**⏱️ Time Range:** {decomp_res.time_range}")
                st.markdown(
                    "**🔍 Keyword Vectors:** "
                    + " ".join([f"`{k}`" for k in decomp_res.search_keywords])
                )

    # 4. Specialist Deep-Dive Mode
    elif research_mode == "📚 Specialist Deep-Dive":
        st.subheader("📚 Specialist Deep-Dive (Direct Sub-Agent Query)")
        st.caption(
            "Query Sub-Agent 1 (Literature Evidence) or Sub-Agent 2 (Society Guidelines) in isolation."
        )

        spec_mode = st.segmented_control(
            "Target Specialist Sub-Agent:",
            [
                "Sub-Agent 1: Evidence Specialist (PubMed/RCTs)",
                "Sub-Agent 2: Guideline Specialist (Societies)",
            ],
            default="Sub-Agent 1: Evidence Specialist (PubMed/RCTs)",
        )

        spec_query = st.text_input(
            "Target Query:",
            value="Prehabilitation in elective colorectal surgery",
            key="spec_query_input",
        )

        if st.button("🔎 Query Specialist", type="primary"):
            with st.spinner("Querying specialist agent..."):
                is_evid = "Evidence Specialist" in (spec_mode or "")
                req = MultiAgentConsensusRequest(
                    question=spec_query,
                    model=params["model_id"],
                    enable_evidence_agent=is_evid,
                    enable_guideline_agent=not is_evid,
                    thinking_level=params.get("thinking_level"),
                    thinking_budget=params.get("thinking_budget"),
                    mock_mode=params["mock_mode"],
                )
                spec_resp = run_multiagent(req)

            if is_evid:
                st.markdown(spec_resp.evidence_findings.get("summary", "No findings."))
                for s in spec_resp.evidence_findings.get("key_study_findings", []):
                    st.markdown(
                        f"- **[{s.get('study_title')}]({s.get('url')})** — *{s.get('evidence_type')}* ({s.get('year')})"
                    )
            else:
                st.markdown(spec_resp.guideline_findings.get("summary", "No findings."))
                for g in spec_resp.guideline_findings.get("guideline_statements", []):
                    st.markdown(
                        f"- **[{g.get('organization')} — {g.get('guideline_title')}]({g.get('url')})** ({g.get('year')})"
                    )


# -----------------------------------------------------------------------------
# TAB 2: Multimodal Vision & Video Studio
# -----------------------------------------------------------------------------
with tab_multimodal:
    st.subheader("🖼️ Multimodal Vision & Video Studio")
    st.caption(
        "Demonstrates multimodal vision-language understanding on static radiographs, "
        "surgical schematics (e.g., Strasberg Critical View of Safety), and dynamic echocardiogram / ultrasound video clips."
    )

    media_mode = st.segmented_control(
        "Multimodal Inspection Mode:",
        options=[
            "🖼️ Static Vision & Schematics",
            "🎬 Dynamic Ultrasound & Video",
        ],
        default="🖼️ Static Vision & Schematics",
        label_visibility="collapsed",
    )

    if media_mode == "🖼️ Static Vision & Schematics":
        vis_left, vis_right = st.columns([1, 1])

        with vis_left:
            st.markdown("#### 1. Image Source")
            image_source = st.segmented_control(
                "Select Image Source:",
                ["Preset Clinical Imagery & Schematics", "Upload Custom Image"],
                default="Preset Clinical Imagery & Schematics",
                key="vis_img_source",
            )

            image_bytes: Optional[bytes] = None
            image_filename = "radiograph.jpeg"
            image_mime = "image/jpeg"
            active_preset_id: Optional[str] = None
            preset_obj: Optional[Any] = None

            if image_source == "Preset Clinical Imagery & Schematics":
                preset_options = {p.id: f"{p.title} ({p.filename})" for p in preset_images}
                selected_preset_id = st.selectbox(
                    "Choose Preset Image:",
                    options=list(preset_options.keys()),
                    format_func=lambda x: preset_options[x],
                    key="vis_preset_select",
                )
                image_bytes = local_service.get_preset_image_bytes(selected_preset_id)
                preset_obj = next(p for p in preset_images if p.id == selected_preset_id)
                active_preset_id = selected_preset_id
                image_filename = preset_obj.filename
                guessed_mime, _ = mimetypes.guess_type(preset_obj.filename)
                image_mime = guessed_mime or "image/jpeg"
                st.caption(f"📝 {preset_obj.description}")
            else:
                uploaded_file = st.file_uploader(
                    "Upload Medical / Surgical Image (PNG, JPG, WEBP):",
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
                    caption=f"Visual Input: {image_filename} ({pil_img.width}x{pil_img.height} px, {len(image_bytes) / 1024:.1f} KB)",
                    width="stretch",
                )

        with vis_right:
            st.markdown("#### 2. Prompt & Inquiry")

            # Dynamic prompts based on selected preset image
            if preset_obj and getattr(preset_obj, "suggested_prompts", None):
                quick_prompts = list(preset_obj.suggested_prompts) + ["Custom User Prompt..."]
            else:
                quick_prompts = [
                    "Describe only the observable visual anatomical and radiological features in this image.",
                    "Detail the key findings, margins, alignment, and technical aspects visible.",
                    "Custom User Prompt...",
                ]

            selected_prompt_template = st.selectbox(
                "Quick Prompt Presets:",
                options=quick_prompts,
                index=0,
                key="vis_prompt_select",
            )

            if selected_prompt_template == "Custom User Prompt...":
                default_prompt_text = "What anatomical structures and radiological findings are visible?"
            else:
                default_prompt_text = selected_prompt_template

            user_prompt = st.text_area(
                "Inquiry Prompt:",
                value=default_prompt_text,
                height=130,
                key="vis_user_prompt",
            )

            st.caption("🔒 Safety: Responses are strictly educational and non-diagnostic.")

            run_multimodal_btn = st.button(
                "🚀 Run Vision Analysis", type="primary", width="stretch"
            )

        if run_multimodal_btn:
            if not image_bytes:
                st.error("Please provide or select an image asset first.")
            else:
                with st.spinner(
                    f"Analyzing visual features using {params['model_info'].display_name}..."
                ):
                    req = MultimodalInquiryRequest(
                        prompt=user_prompt,
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
                    ["📝 Observation & Analysis", "⚙️ Generation Parameters", "📦 Raw JSON Payload"]
                )

                with resp_tab1:
                    st.markdown(vis_resp.text)
                    if vis_resp.visual_elements_detected:
                        st.markdown("**Detected Anatomical Features:**")
                        st.write(", ".join([f"`{el}`" for el in vis_resp.visual_elements_detected]))
                    st.caption(
                        f"⏱️ Latency: **{vis_resp.latency_ms:.1f} ms** | Model: **{vis_resp.model}**"
                    )

                with resp_tab2:
                    st.markdown(
                        f"""
                        - **Model ID:** `{vis_resp.model}`
                        - **Latency:** `{vis_resp.latency_ms} ms`
                        - **Estimated Tokens:** `{vis_resp.token_estimate}`
                        - **Thinking Level:** `{params.get("thinking_level") or "N/A"}`
                        - **Thinking Budget:** `{params.get("thinking_budget") if params.get("thinking_budget") is not None else "N/A"}`
                        - **Temperature:** `{params["temperature"]}`
                        - **Top-P:** `{params["top_p"]}`
                        - **Max Tokens:** `{params["max_output_tokens"]}`
                        """
                    )
                    st.code(user_prompt, language="markdown")

                with resp_tab3:
                    st.json(vis_resp.model_dump())

    elif media_mode == "🎬 Dynamic Ultrasound & Video":
        vid_left, vid_right = st.columns([1, 1])

        with vid_left:
            st.markdown("#### 1. Video Source")
            video_source = st.segmented_control(
                "Select Video Source:",
                ["Preset Clinical Video (Echo / Ultrasound)", "Upload Custom Video"],
                default="Preset Clinical Video (Echo / Ultrasound)",
                key="vid_source_radio",
            )

            video_bytes: Optional[bytes] = None
            video_filename = "apical_4_chamber_echo.mp4"
            video_mime = "video/mp4"
            active_video_id: Optional[str] = None
            preset_vid_obj: Optional[Any] = None

            if video_source == "Preset Clinical Video (Echo / Ultrasound)":
                preset_vid_options = {v.id: f"{v.title} ({v.filename})" for v in preset_videos}
                selected_vid_id = st.selectbox(
                    "Choose Preset Video:",
                    options=list(preset_vid_options.keys()),
                    format_func=lambda x: preset_vid_options[x],
                    key="vid_preset_select",
                )
                video_bytes = local_service.get_preset_video_bytes(selected_vid_id)
                preset_vid_obj = next(v for v in preset_videos if v.id == selected_vid_id)
                active_video_id = selected_vid_id
                video_filename = preset_vid_obj.filename
                guessed_mime, _ = mimetypes.guess_type(preset_vid_obj.filename)
                video_mime = guessed_mime or "video/mp4"
                st.caption(f"📝 {preset_vid_obj.description}")
            else:
                uploaded_vid = st.file_uploader(
                    "Upload Medical Video Clip (MP4, WEBM, MOV - max 20MB):",
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
                    f"🎬 Clip: `{video_filename}` ({len(video_bytes) / 1024:.1f} KB, format: `{video_mime}`)"
                )

        with vid_right:
            st.markdown("#### 2. Temporal Prompt & Inquiry")

            if preset_vid_obj and getattr(preset_vid_obj, "suggested_prompts", None):
                quick_vid_prompts = list(preset_vid_obj.suggested_prompts) + ["Custom User Prompt..."]
            else:
                quick_vid_prompts = [
                    "Describe the observable cardiac structures and dynamic wall motion in this echocardiogram video clip.",
                    "Evaluate the contraction and symmetry of the left ventricle vs right ventricle across the cardiac cycle.",
                    "Custom User Prompt...",
                ]

            selected_vid_prompt = st.selectbox(
                "Quick Video Prompt Presets:",
                options=quick_vid_prompts,
                index=0,
                key="vid_prompt_select",
            )

            if selected_vid_prompt == "Custom User Prompt...":
                default_vid_text = (
                    "What dynamic anatomical movements and wall motion patterns are observable in this clip?"
                )
            else:
                default_vid_text = selected_vid_prompt

            user_vid_prompt = st.text_area(
                "Temporal Inquiry Prompt:",
                value=default_vid_text,
                height=130,
                key="vid_user_prompt",
            )

            st.caption("🔒 Safety: Video analysis is strictly for education/research; non-diagnostic.")

            run_video_btn = st.button(
                "🚀 Run Video Multimodal Analysis",
                type="primary",
                width="stretch",
                key="run_video_btn",
            )

        if run_video_btn:
            if not video_bytes:
                st.error("Please provide or select a video clip first.")
            else:
                with st.spinner(
                    f"Analyzing video temporal frames using {params['model_info'].display_name}..."
                ):
                    req = MultimodalInquiryRequest(
                        prompt=user_vid_prompt,
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
                    ["📝 Temporal Observation & Analysis", "⚙️ Generation Parameters", "📦 Raw JSON Payload"]
                )

                with v_tab1:
                    st.markdown(vid_resp.text)
                    if vid_resp.visual_elements_detected:
                        st.markdown("**Detected Dynamic Anatomical Structures:**")
                        st.write(", ".join([f"`{el}`" for el in vid_resp.visual_elements_detected]))
                    st.caption(
                        f"⏱️ Latency: **{vid_resp.latency_ms:.1f} ms** | Model: **{vid_resp.model}**"
                    )

                with v_tab2:
                    st.markdown(
                        f"""
                        - **Model ID:** `{vid_resp.model}`
                        - **Latency:** `{vid_resp.latency_ms} ms`
                        - **Estimated Tokens:** `{vid_resp.token_estimate}`
                        - **Thinking Level:** `{params.get("thinking_level") or "N/A"}`
                        - **Thinking Budget:** `{params.get("thinking_budget") if params.get("thinking_budget") is not None else "N/A"}`
                        - **Temperature:** `{params["temperature"]}`
                        - **Top-P:** `{params["top_p"]}`
                        - **Max Tokens:** `{params["max_output_tokens"]}`
                        """
                    )
                    st.code(user_vid_prompt, language="markdown")

                with v_tab3:
                    st.json(vid_resp.model_dump())


# -----------------------------------------------------------------------------
# TAB 3: API & Diagnostics
# -----------------------------------------------------------------------------
with tab_diagnostics:
    st.subheader("⚙️ System Diagnostics & Backend Health")

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown("#### FastAPI REST Health Check")
        try:
            with httpx.Client(timeout=3.0) as client:
                res = client.get(f"{params['fastapi_url']}/api/health")
                if res.status_code == 200:
                    st.success("✅ FastAPI Backend is ONLINE and responding!")
                    st.json(res.json())
                else:
                    st.warning(f"FastAPI responded with HTTP {res.status_code}")
        except Exception as ex:
            st.error(
                f"❌ FastAPI Backend is currently unreachable at `{params['fastapi_url']}` ({ex})."
            )
            st.caption(
                "You can run the backend using: `uv run uvicorn app.backend.api:app --reload --port 8000`"
            )

    with d_col2:
        st.markdown("#### Token Optimization & Best Practices")
        st.info(
            """
            - **Zero-Token Offline Mode:** When testing locally or demonstrating UI components, keep
              *Zero-Token Offline Mode* checked in the sidebar to prevent unnecessary Gemini API calls.
            - **Thinking Budget:** For models like `gemini-2.5-pro` and `gemini-2.5-flash`, adjust the
              thinking budget slider to balance response depth vs token economy.
            - **Sub-Agent Toggles:** Disable unused sub-agents when you only need literature or guidelines.
            """
        )

        st.markdown("#### Environment Diagnostics")
        has_key = bool(os.environ.get("GOOGLE_API_KEY"))
        has_proj = bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))
        st.write(f"- `GOOGLE_API_KEY`: {'Configured ✅' if has_key else 'Not set ❌'}")
        st.write(f"- `GOOGLE_CLOUD_PROJECT`: {'Configured ✅' if has_proj else 'Not set ❌'}")
        st.write(f"- `Active Model`: `{params['model_id']}`")
