# Gemini 3.8 Model Baseline Manifest

- **Document Version**: 1.0.0
- **Status**: **VERIFIED & TESTED MODEL BASELINE**
- **Date**: 2026-10-03
- **GCP Project**: Configured via `GOOGLE_CLOUD_PROJECT`
- **Target Model**: `gemini-3.8-flash`
- **Target Location**: `us` (multi-region endpoint)

---

## 1. Official Documentation & Specifications

| Dimension | Specification | Verification Notes & Official References |
| :--- | :--- | :--- |
| **Model Name** | `gemini-3.8-flash` | Official identifier in Google GenAI SDK and Vertex AI. |
| **Launch Stage** | Generally Available (GA) | Production-grade "intelligent workhorse" model. |
| **Release Date** | Early 2026 | Succeeded Gemini 2.5/3.7 for high-efficiency agentic workflows. |
| **Retirement Status** | Active (Current Baseline) | Supported through standard lifecycle; introductory pricing through Dec 31, 2026. |
| **Supported Regions** | `us` (multi-region), `eu` (multi-region), `global` | **Critical Finding**: Single-region `us-central1` returns `404 NOT_FOUND`. Multi-region `us` and `global` endpoints are fully supported. |
| **Context Window** | 1,048,576 tokens (Input) / 65,536 tokens (Output) | Full 1M token context window. |
| **Search Grounding** | **Supported & Verified** | Live Google Search grounding tool (`google.adk.tools.google_search`) verified functional. |
| **URL Context** | **Supported** | Supported via GenAI SDK / Agent Studio context tools. |
| **Structured Output** | **Supported & Verified** | Native JSON Schema and Pydantic model response generation supported. |
| **Agent Studio Availability** | **Supported & Verified** | Selectable model in Agent Studio within `us` and `global` locations. |
| **ADK Compatibility** | **Supported & Verified** | Verified 100% compatible with `google-adk 2.11.0` and `google-genai 2.28.0`. |
| **Supported Thinking Levels** | `LOW`, `MEDIUM`, `HIGH` | **Critical Finding**: Replaces `thinking_budget`. `MINIMAL` is **NOT supported** (causes API validation error). `MEDIUM` is the recommended standard baseline. |
| **Sampling Parameters** | **Deprecated & Removed** | **Critical Finding**: `temperature`, `top_p`, and `top_k` are deprecated and ignored by the Gemini 3.8 Flash backend. Reasoning depth and determinism are controlled exclusively via `thinking_level`. All legacy sampling parameters must be omitted from `GenerateContentConfig`. |
| **Pricing** | $0.75 / 1M input, $3.75 / 1M output | Introductory tier through Dec 31, 2026 ($1.50 / $7.50 thereafter). |

---

## 2. Official Documentation Reference Sources

1. **Model Overview & Capabilities**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models/gemini-3-8-flash
   - https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
2. **Location & Regional Endpoints**:
   - https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations
   - https://cloud.google.com/vertex-ai/docs/general/locations
3. **Thinking Configuration & Levels**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/thinking-config
4. **Search Grounding**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-with-google-search

---

## 3. Actual Model Access Verification Across Locations

Using Google Cloud Application Default Credentials (ADC), model access tests were verified across candidate locations:

```text
Location us-central1: FAILED -> 404 NOT_FOUND
  (Publisher model `projects/<project-id>/locations/us-central1/publishers/google/models/gemini-3.8-flash` was not found)

Location us: SUCCESS -> PING_OK
  (Multi-region US endpoint responds with low latency and valid inference)

Location global: SUCCESS -> PING_OK
  (Global endpoint responds with valid inference)
```

### Location Decision
- **Chosen Location**: `us`
- **Rationale**: `us-central1` is not populated with the `gemini-3.8-flash` publisher endpoint. Multi-region `us` encompasses `us-central1`, preserves US data boundary guarantees, offers high availability across US data centers, and responds with low latency.
