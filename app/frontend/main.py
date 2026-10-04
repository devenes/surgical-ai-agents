"""Streamlit Main Application for Surgical AI Studio (FastAPI + Streamlit).

Supports multimodal image understanding and a 2-subagent (Evidence & Guideline)
orchestration pipeline with token-optimized offline mode and interactive tabs.
"""

import base64
import io
import os
from typing import Optional
import httpx
from PIL import Image
import streamlit as st

from app.backend.schemas import (
    MultiAgentConsensusRequest,
    MultiAgentConsensusResponse,
    MultimodalInquiryRequest,
    MultimodalInquiryResponse,
    PICOTDecomposeRequest,
)
from app.backend.service import AppService
from app.frontend.components import (
    render_consensus_matrix,
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


# =============================================================================
# Main Header
# =============================================================================
st.header("🩺 Surgical AI Studio: Multimodal & Multi-Agent Research", divider="rainbow")
st.caption(
    "Interactive research workspace built with **FastAPI** + **Streamlit** | "
    "Features **Multimodal Image Vision** and a **2-Subagent Architecture** "
    "(Evidence Specialist + Guideline Specialist) managed by a Coordinator."
)

# Quick stats / status badges in top container
badge_col1, badge_col2, badge_col3, badge_col4 = st.columns(4)
with badge_col1:
    st.info(f"🧠 **Model:** `{params['model_info'].display_name}`")
with badge_col2:
    mode_text = "⚡ Zero-Token Offline" if params["mock_mode"] else "🌐 Live Vertex AI"
    st.success(f"🔌 **Mode:** `{mode_text}`")
with badge_col3:
    st.info(f"⚙️ **Backend:** `{params['connection_mode']}`")
with badge_col4:
    agents_count = int(params["enable_evidence"]) + int(params["enable_guideline"])
    st.info(f"🤖 **Sub-Agents:** `{agents_count} Active`")


# =============================================================================
# Application Tabs
# =============================================================================
tab_vision, tab_multiagent, tab_picot, tab_specialist, tab_diagnostics = st.tabs(
    [
        "👁️ Multimodal Vision Studio",
        "🤖 Multi-Agent Consensus Studio",
        "⚡ PICOT Query Decomposer",
        "📚 Specialist Deep-Dive",
        "⚙️ API & Diagnostics",
    ]
)


# -----------------------------------------------------------------------------
# TAB 1: Multimodal Vision Studio
# -----------------------------------------------------------------------------
with tab_vision:
    st.subheader("🖼️ Surgical & Anatomical Vision Inspection")
    st.markdown(
        "Demonstrates multimodal vision-language understanding. Upload surgical imagery "
        "or inspect pre-bundled schematics (such as the *Critical View of Safety* in laparoscopic cholecystectomy)."
    )

    vis_left, vis_right = st.columns([1, 1])

    with vis_left:
        st.markdown("#### 1. Image Source")
        image_source = st.radio(
            "Select Image Source:",
            ["Preset Surgical Schematic", "Upload Custom Image"],
            horizontal=True,
            key="vis_img_source",
        )

        image_bytes: Optional[bytes] = None
        image_filename = "preset_schematic.png"
        image_mime = "image/png"

        if image_source == "Preset Surgical Schematic":
            preset_options = {p.id: f"{p.title} ({p.filename})" for p in preset_images}
            selected_preset_id = st.selectbox(
                "Choose Preset Schematic:",
                options=list(preset_options.keys()),
                format_func=lambda x: preset_options[x],
            )
            image_bytes = local_service.get_preset_image_bytes(selected_preset_id)
            preset_obj = next(p for p in preset_images if p.id == selected_preset_id)
            st.caption(f"📝 {preset_obj.description}")
        else:
            uploaded_file = st.file_uploader(
                "Upload Surgical Image (PNG, JPG, WEBP):",
                type=["png", "jpg", "jpeg", "webp"],
                key="vis_file_uploader",
            )
            if uploaded_file is not None:
                image_bytes = uploaded_file.getvalue()
                image_filename = uploaded_file.name
                image_mime = uploaded_file.type or "image/png"

        if image_bytes:
            pil_img = Image.open(io.BytesIO(image_bytes))
            st.image(
                pil_img,
                caption=f"Visual Input: {image_filename} ({pil_img.width}x{pil_img.height} px, {len(image_bytes)/1024:.1f} KB)",
                use_container_width=True,
            )

    with vis_right:
        st.markdown("#### 2. Prompt & Inquiry")

        # Quick prompt selector
        quick_prompts = [
            "Describe only the observable visual anatomical and operative features in this image.",
            "Identify the 3 criteria of the Critical View of Safety (CVS) depicted here.",
            "Explain what computer-vision research tasks could use this visual information.",
            "Custom User Prompt...",
        ]

        selected_prompt_template = st.selectbox(
            "Quick Prompt Presets:",
            options=quick_prompts,
            index=0,
            key="vis_prompt_select",
        )

        if selected_prompt_template == "Custom User Prompt...":
            default_prompt_text = "What anatomical structures and surgical planes are visible?"
        else:
            default_prompt_text = selected_prompt_template

        user_prompt = st.text_area(
            "Inquiry Prompt:",
            value=default_prompt_text,
            height=130,
            key="vis_user_prompt",
        )

        st.caption("🔒 Safety: Responses are strictly educational and non-diagnostic.")

        run_multimodal_btn = st.button("🚀 Run Vision Analysis", type="primary", use_container_width=True)

    if run_multimodal_btn:
        if not image_bytes:
            st.error("Please provide or select an image asset first.")
        else:
            with st.spinner(f"Analyzing visual features using {params['model_info'].display_name}..."):
                req = MultimodalInquiryRequest(
                    prompt=user_prompt,
                    image_base64=base64.b64encode(image_bytes).decode("utf-8"),
                    image_mime_type=image_mime,
                    model=params["model_id"],
                    temperature=params["temperature"],
                    top_p=params["top_p"],
                    max_output_tokens=params["max_output_tokens"],
                    thinking_budget=params["thinking_budget"],
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
                st.caption(f"⏱️ Latency: **{vis_resp.latency_ms:.1f} ms** | Model: **{vis_resp.model}**")

            with resp_tab2:
                st.markdown(
                    f"""
                    - **Model ID:** `{vis_resp.model}`
                    - **Latency:** `{vis_resp.latency_ms} ms`
                    - **Estimated Tokens:** `{vis_resp.token_estimate}`
                    - **Temperature:** `{params['temperature']}`
                    - **Top-P:** `{params['top_p']}`
                    - **Max Tokens:** `{params['max_output_tokens']}`
                    - **Thinking Budget:** `{params['thinking_budget']}`
                    """
                )
                st.code(user_prompt, language="markdown")

            with resp_tab3:
                st.json(vis_resp.model_dump())


# -----------------------------------------------------------------------------
# TAB 2: Multi-Agent Consensus Studio
# -----------------------------------------------------------------------------
with tab_multiagent:
    st.subheader("🤖 Multi-Agent Consensus Architecture")
    st.markdown(
        "Orchestrates a **Coordinator Agent** delegating research in parallel to two specialized sub-agents:\n"
        "- **Sub-Agent 1 (Evidence Specialist):** Searches and synthesizes peer-reviewed randomized trials (PubMed).\n"
        "- **Sub-Agent 2 (Guideline Specialist):** Reviews clinical practice guidelines from major surgical societies (ASCRS, ERAS, SAGES).\n"
        "- **Coordinator Synthesis:** Normalizes inquiry into PICOT, reconciles agreements/divergences, and generates consensus matrix."
    )

    preset_titles = {p.id: f"{p.title} ({p.category})" for p in preset_questions}
    selected_preset_qid = st.selectbox(
        "Choose Preset Surgical Topic or Customize Below:",
        options=list(preset_titles.keys()),
        format_func=lambda x: preset_titles[x],
        key="ma_preset_select",
    )

    active_preset = next(p for p in preset_questions if p.id == selected_preset_qid)

    research_question = st.text_area(
        "Clinical Research Question:",
        value=active_preset.question,
        height=100,
        key="ma_question_input",
    )

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        run_consensus_btn = st.button("🚀 Execute Multi-Agent Consensus", type="primary", use_container_width=True)
    with col_info:
        active_subagents = []
        if params["enable_evidence"]:
            active_subagents.append("📚 Evidence Specialist")
        if params["enable_guideline"]:
            active_subagents.append("📋 Guideline Specialist")
        st.caption(f"Active Pipeline: Coordinator ➔ {' + '.join(active_subagents) or 'None'}")

    if run_consensus_btn:
        with st.spinner("Executing multi-agent research workflow (Coordinator + Sub-Agents)..."):
            agent_req = MultiAgentConsensusRequest(
                question=research_question,
                model=params["model_id"],
                enable_evidence_agent=params["enable_evidence"],
                enable_guideline_agent=params["enable_guideline"],
                mock_mode=params["mock_mode"],
            )
            agent_resp = run_multiagent(agent_req)

        st.divider()

        # Step Timeline
        render_execution_timeline(agent_resp.execution_steps)

        # Normalized PICOT Scope Expander
        with st.expander("📌 View Normalized PICOT Scope", expanded=True):
            p_cols = st.columns(4)
            with p_cols[0]:
                st.markdown(f"**Population:**\n\n{agent_resp.normalized_picot.get('population', '')}")
            with p_cols[1]:
                st.markdown(f"**Intervention:**\n\n{agent_resp.normalized_picot.get('intervention', '')}")
            with p_cols[2]:
                st.markdown(f"**Comparator:**\n\n{agent_resp.normalized_picot.get('comparator', '')}")
            with p_cols[3]:
                st.markdown(f"**Outcomes:**\n\n{', '.join(agent_resp.normalized_picot.get('outcomes', []))}")

        # Side-by-Side Specialist Findings
        render_evidence_vs_guidelines(
            agent_resp.evidence_findings,
            agent_resp.guideline_findings,
        )

        # Consensus & Discrepancy Matrix
        render_consensus_matrix(agent_resp.consensus_matrix)

        # Final Master Synthesis
        st.markdown("### 📝 Master Evidence Brief")
        st.markdown(agent_resp.final_synthesis)

        # Verified Sources
        if agent_resp.sources:
            st.markdown("#### 🔗 Verified Citations")
            for src in agent_resp.sources:
                st.markdown(f"- [{src.get('title')}]({src.get('url')}) `({src.get('type')})`")

        st.caption(f"ℹ️ {agent_resp.safety_disclaimer}")


# -----------------------------------------------------------------------------
# TAB 3: PICOT Query Decomposer
# -----------------------------------------------------------------------------
with tab_picot:
    st.subheader("⚡ PICOT Query Decomposer (Sub-Agent 1 Utility)")
    st.markdown(
        "Deconstructs complex, ambiguous clinical questions into standardized epidemiological "
        "**PICOT** (Population, Intervention, Comparator, Outcomes, Timeline) search vectors."
    )

    decom_input = st.text_area(
        "Enter raw surgical inquiry:",
        value=(
            "What does recent evidence say about robotic vs laparoscopic mesh repair for ventral "
            "and incisional hernias in obese adults regarding surgical site occurrences and return to work?"
        ),
        height=100,
        key="picot_decomp_input",
    )

    if st.button("🧩 Decompose Inquiry", type="primary"):
        with st.spinner("Extracting PICOT parameters..."):
            decomp_res = local_service.decompose_picot(
                PICOTDecomposeRequest(question=decom_input, model=params["model_id"], mock_mode=True)
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
                "**🔍 Keyword Vectors:** " + " ".join([f"`{k}`" for k in decomp_res.search_keywords])
            )


# -----------------------------------------------------------------------------
# TAB 4: Specialist Deep-Dive
# -----------------------------------------------------------------------------
with tab_specialist:
    st.subheader("📚 Specialist Deep-Dive (Direct Sub-Agent Query)")
    st.markdown("Query Sub-Agent 1 (Literature Evidence) or Sub-Agent 2 (Society Guidelines) in isolation.")

    spec_mode = st.radio(
        "Select Target Specialist Sub-Agent:",
        ["Sub-Agent 1: Evidence Specialist (PubMed/RCTs)", "Sub-Agent 2: Guideline Specialist (Societies)"],
        horizontal=True,
    )

    spec_query = st.text_input(
        "Target Query:",
        value="Prehabilitation in elective colorectal surgery",
        key="spec_query_input",
    )

    if st.button("🔎 Query Specialist", type="primary"):
        with st.spinner("Querying specialist agent..."):
            # Execute targeted request using our service
            is_evid = "Evidence Specialist" in spec_mode
            req = MultiAgentConsensusRequest(
                question=spec_query,
                model=params["model_id"],
                enable_evidence_agent=is_evid,
                enable_guideline_agent=not is_evid,
                mock_mode=params["mock_mode"],
            )
            spec_resp = run_multiagent(req)

        if is_evid:
            st.markdown(spec_resp.evidence_findings.get("summary", "No findings."))
            for s in spec_resp.evidence_findings.get("key_study_findings", []):
                st.markdown(f"- **[{s.get('study_title')}]({s.get('url')})** — *{s.get('evidence_type')}* ({s.get('year')})")
        else:
            st.markdown(spec_resp.guideline_findings.get("summary", "No findings."))
            for g in spec_resp.guideline_findings.get("guideline_statements", []):
                st.markdown(f"- **[{g.get('organization')} — {g.get('guideline_title')}]({g.get('url')})** ({g.get('year')})")


# -----------------------------------------------------------------------------
# TAB 5: API & Diagnostics
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
            st.error(f"❌ FastAPI Backend is currently unreachable at `{params['fastapi_url']}` ({ex}).")
            st.caption("You can run the backend using: `uv run uvicorn app.backend.api:app --reload --port 8000`")

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
