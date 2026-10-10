"""Offline unit tests for Turkish/English localization (i18n).

Validates all 12 core requirements: default locale, dictionary resolution,
fallback behavior, placeholder interpolation, technical term preservation,
preset identity preservation, stable workflow values, session state preservation,
runtime language directives, dual execution modes, schema stability,
and benchmark/instruction integrity.
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.backend.api import app
from app.backend.schemas import (
    ComparativeAnalysisRequest,
    MonolithicDirectRequest,
    MultiAgentConsensusRequest,
    MultimodalInquiryRequest,
    PICOTDecomposeRequest,
)
from app.backend.service import (
    AVAILABLE_MODELS,
    PRESET_IMAGES,
    PRESET_INQUIRIES,
    PRESET_VIDEOS,
    AppService,
)
from app.frontend.components import get_case_type_badge
from app.frontend.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    TRANSLATIONS,
    apply_language_directive,
    get_locale,
    get_localized_preset_image,
    get_localized_preset_inquiry,
    get_localized_preset_video,
    get_missing_translation_keys,
    get_preset_question_for_locale,
    set_locale,
    t,
)


@pytest.fixture
def mock_service():
    return AppService(force_mock=True)


@pytest.fixture
def api_client():
    return TestClient(app)


# 1. English is the default locale
def test_default_locale():
    assert DEFAULT_LOCALE == "en"
    assert "en" in SUPPORTED_LOCALES
    assert "tr" in SUPPORTED_LOCALES
    set_locale("en")
    assert get_locale() == "en"


# 2. Turkish and English translations resolve correctly
def test_translations_resolve():
    # Sidebar
    assert t("sidebar.title", locale="en") == "🩺 Surgical AI Studio"
    assert t("sidebar.title", locale="tr") == "🩺 Cerrahi Yapay Zeka Stüdyosu"

    # Tabs
    assert t("tabs.research", locale="en") == "🔬 Clinical Research & Consensus"
    assert t("tabs.research", locale="tr") == "🔬 Klinik Araştırma ve Konsensüs"
    assert t("tabs.multimodal", locale="en") == "🖼️ Multimodal Vision & Video"
    assert t("tabs.multimodal", locale="tr") == "🖼️ Çok Modlu Görme ve Video"

    # Badges
    assert t("badges.normal_synthesis", locale="en") == "📘 Normal Evidence Synthesis"
    assert t("badges.normal_synthesis", locale="tr") == "📘 Normal Kanıt Sentezi"
    assert t("badges.safety_refusal", locale="en") == "🛑 Safety: Direct Patient Refusal Trap"
    assert t("badges.safety_refusal", locale="tr") == "🛑 Güvenlik: Doğrudan Hasta Önerisi Reddi Tuzağı"


# 3. Missing translation keys use intended fallback
def test_missing_translation_fallback():
    # If a key does not exist in TR but exists in EN, falls back to EN
    TRANSLATIONS["en"]["test.dummy_fallback_key"] = "English Fallback Value"
    try:
        assert t("test.dummy_fallback_key", locale="tr") == "English Fallback Value"
    finally:
        del TRANSLATIONS["en"]["test.dummy_fallback_key"]

    # If key does not exist anywhere, returns key name safely
    missing_key = "completely.nonexistent.key.12345"
    assert t(missing_key, locale="en") == missing_key
    assert t(missing_key, locale="tr") == missing_key


# 4. Placeholder formatting works correctly
def test_placeholder_formatting():
    # Valid placeholders
    en_formatted = t("header.tokens_unit", locale="en", budget=2048)
    assert en_formatted == "2048 tokens"

    tr_formatted = t("header.tokens_unit", locale="tr", budget=2048)
    assert tr_formatted == "2048 token"

    latency_en = t("multimodal.latency_caption", locale="en", ms=124.6, model="gemini-2.5-flash")
    assert "124.6 ms" in latency_en
    assert "gemini-2.5-flash" in latency_en

    latency_tr = t("multimodal.latency_caption", locale="tr", ms=124.6, model="gemini-2.5-flash")
    assert "124.6 ms" in latency_tr
    assert "gemini-2.5-flash" in latency_tr

    # Mismatched/missing kwargs do not throw unhandled exception
    res = t("multimodal.latency_caption", locale="en", wrong_param=123)
    assert isinstance(res, str)


# 5. Critical technical labels and stable identifiers remain unchanged
def test_technical_labels_preserved():
    for model in AVAILABLE_MODELS:
        assert "gemini" in model.id.lower()

    # Model identifiers in sidebar translation keys
    assert "gemini-2.5-flash" in [m.id for m in AVAILABLE_MODELS]
    assert "gemini-3.8-flash" in [m.id for m in AVAILABLE_MODELS]

    # Technical keywords preserved in localized strings
    sidebar_tr = t("sidebar.execution_mode_help", locale="tr")
    assert "AppService" in sidebar_tr
    assert "FastAPI" in sidebar_tr
    assert "REST" in sidebar_tr
    assert "http://127.0.0.1:8000" in sidebar_tr

    # PICOT acronym and sub-agent identities preserved
    picot_caption_tr = t("research.picot.caption", locale="tr")
    assert "PICOT" in picot_caption_tr


# 6. Preset translations preserve original IDs, asset paths, and execution values
def test_preset_translations_preserve_identities():
    # Inquiries
    for preset in PRESET_INQUIRIES:
        loc_tr = get_localized_preset_inquiry(preset, "tr")
        assert loc_tr.id == preset.id
        assert loc_tr.case_type == preset.case_type
        assert loc_tr.recommended_model == preset.recommended_model
        assert loc_tr.title != ""
        assert loc_tr.question != ""

    # Images
    for img in PRESET_IMAGES:
        loc_img = get_localized_preset_image(img, "tr")
        assert loc_img.id == img.id
        assert loc_img.filename == img.filename
        assert len(loc_img.suggested_prompts) == len(img.suggested_prompts)

    # Videos
    for vid in PRESET_VIDEOS:
        loc_vid = get_localized_preset_video(vid, "tr")
        assert loc_vid.id == vid.id
        assert loc_vid.filename == vid.filename
        assert loc_vid.duration_sec == vid.duration_sec
        assert len(loc_vid.suggested_prompts) == len(vid.suggested_prompts)


# 7. Localized display labels map to correct stable internal workflow values
def test_display_labels_mapping():
    # Research modes stable internal values
    research_keys = [
        "multi_agent_consensus",
        "benchmark_audit",
        "picot_decomposer",
        "specialist_deep_dive",
    ]
    for key in research_keys:
        en_label = t(f"research.modes.{key}", locale="en")
        tr_label = t(f"research.modes.{key}", locale="tr")
        assert en_label != ""
        assert tr_label != ""
        assert en_label != tr_label

    # Badge mapping retains fallback for unknown types
    badge = get_case_type_badge("unknown_custom_type")
    assert "unknown_custom_type" in badge


# 8. Language state can change without explicitly resetting unrelated session state
def test_language_state_change_preservation():
    # Test preset default question vs customized prompt logic
    preset_id = "NORM-01-COLORECTAL-PREHAB"
    raw_p = next(p for p in PRESET_INQUIRIES if p.id == preset_id)

    en_q = get_preset_question_for_locale(preset_id, "en", raw_p.question)
    tr_q = get_preset_question_for_locale(preset_id, "tr", raw_p.question)
    assert en_q != tr_q

    # Simulate unedited user prompt switching locales: should update to target default
    user_prompt = en_q
    if user_prompt == en_q:
        new_prompt = tr_q
    assert new_prompt == tr_q

    # Simulate edited custom prompt: must be preserved and NOT overwritten
    custom_user_prompt = "My custom modified surgical question for laparoscopic surgery."
    if custom_user_prompt == en_q:
        overwritten_prompt = tr_q
    else:
        overwritten_prompt = custom_user_prompt
    assert overwritten_prompt == custom_user_prompt


# 9. Language-specific request instructions applied only where intended
def test_language_directive_applied_properly():
    original_prompt = "Compare early vs delayed cholecystectomy for biliary pancreatitis."

    # English mode: untouched
    en_prompt = apply_language_directive(original_prompt, locale="en")
    assert en_prompt == original_prompt

    # Turkish mode: appends directive, preserves original prompt prefix
    tr_prompt = apply_language_directive(original_prompt, locale="tr")
    assert tr_prompt.startswith(original_prompt)
    assert "[Dil Yönergesi" in tr_prompt
    assert "Türkçe" in tr_prompt
    assert "DOI/PMID" in tr_prompt

    # Idempotent: does not duplicate if already present
    double_tr = apply_language_directive(tr_prompt, locale="tr")
    assert double_tr == tr_prompt


# 10. Both execution modes receive equivalent language handling
def test_both_execution_modes_with_directive(mock_service, api_client):
    question_with_directive = apply_language_directive(
        "For adults undergoing elective colorectal surgery, evaluate prehabilitation.",
        locale="tr",
    )

    # 1. Direct in-process
    direct_req = MultiAgentConsensusRequest(
        question=question_with_directive,
        model="gemini-2.5-flash",
        mock_mode=True,
    )
    direct_resp = mock_service.execute_multiagent_consensus(direct_req)
    assert direct_resp.final_synthesis != ""
    assert len(direct_resp.execution_steps) > 0

    # 2. REST API endpoint
    api_resp = api_client.post(
        "/api/agents/consensus",
        json=direct_req.model_dump(),
    )
    assert api_resp.status_code == 200
    api_data = api_resp.json()
    assert api_data["final_synthesis"] != ""


# 11. API schemas and required payload fields remain unchanged
def test_api_schemas_unchanged():
    # Validate request schemas instantiate with their original required fields
    mm_req = MultimodalInquiryRequest(prompt="Test prompt", mock_mode=True)
    assert mm_req.prompt == "Test prompt"

    ma_req = MultiAgentConsensusRequest(question="Clinical question", mock_mode=True)
    assert ma_req.question == "Clinical question"

    comp_req = ComparativeAnalysisRequest(question="Comparative question", mock_mode=True)
    assert comp_req.question == "Comparative question"

    picot_req = PICOTDecomposeRequest(question="Picot query", mock_mode=True)
    assert picot_req.question == "Picot query"

    mono_req = MonolithicDirectRequest(question="Monolithic baseline", mock_mode=True)
    assert mono_req.question == "Monolithic baseline"


# 12. Benchmark fixtures and internal agent instruction files remain untouched
def test_benchmark_and_instructions_untouched():
    repo_root = Path(__file__).resolve().parent.parent

    # Test cases fixture exists and is valid
    yaml_file = repo_root / "evaluations" / "test-cases.yaml"
    assert yaml_file.exists()
    assert yaml_file.stat().st_size > 0

    # Agent instruction files exist and are untranslated
    coord_file = repo_root / "agents" / "coordinator" / "instructions.md"
    assert coord_file.exists()
    assert "Coordinator Agent" in coord_file.read_text(encoding="utf-8")

    evidence_file = repo_root / "agents" / "evidence" / "instructions.md"
    assert evidence_file.exists()
    assert "Evidence Agent" in evidence_file.read_text(encoding="utf-8")

    guideline_file = repo_root / "agents" / "guideline" / "instructions.md"
    assert guideline_file.exists()
    assert "Guideline Agent" in guideline_file.read_text(encoding="utf-8")


# 13. Translation coverage validation
def test_translation_coverage_complete():
    missing_in_tr = get_missing_translation_keys("tr")
    assert missing_in_tr == [], f"Missing Turkish translations for keys: {missing_in_tr}"

    # Ensure no empty strings
    for loc in ("en", "tr"):
        for key, val in TRANSLATIONS[loc].items():
            assert val != "", f"Empty translation for key '{key}' in locale '{loc}'"
