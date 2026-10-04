# Application & Interface Layer (Phase 3)

## Purpose

The `app/` directory is reserved for user-facing interactive interfaces and presentation tools for the surgical workshop proof-of-concept.

## Planned Interfaces (Phase 3)

1. **Surgeon Workshop Web UI**:
   - A lightweight interactive web dashboard (e.g., Streamlit, Gradio, or FastAPI + React) allowing surgeons to enter research questions during the live session.
   - Interactive visual inspection of the multi-agent execution timeline (Coordinator decomposition → Evidence & Guideline agent queries → Final synthesis).
   - Side-by-side rendering of:
     - Evidence findings vs. Guideline statements.
     - Consensus matrix (Agreements / Disagreements / Uncertainties).
     - Verified source links.

2. **CLI Runner**:
   - Terminal-based batch evaluation harness to execute prompts from `prompts/demo-questions.md` or `prompts/test-prompts.md`.

## Implementation Status

- **Phase 1 Status**: Scaffolding only. No UI frameworks installed to maintain a minimal initial footprint.
- **Phase 3 Planned**: Minimal local web runner following ADK integration.
