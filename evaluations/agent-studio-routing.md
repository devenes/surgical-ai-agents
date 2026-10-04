# Agent Studio Routing & Orchestration Behavior

- **Document Version**: 1.0.0
- **Evaluation Date**: 2026-10-03
- **Target Platform**: Google Cloud Gemini Enterprise Agent Platform (Agent Studio) & ADK Baseline
- **Observed Model**: `gemini-3.8-flash`
- **Status**: Verified Operational Behavior Analysis

---

## 1. Executive Summary & Core Rules

In multi-agent systems built with LLM orchestrators (such as Gemini 3.8 Flash), routing and delegation decisions are governed by **dynamic model planning** rather than static, hard-coded directed graphs.

### Key Workshop Veracity Rules:
1. **DO NOT PROMISE**: *"The Evidence Agent always runs first."*
2. **DO NOT PROMISE**: *"Subagents execute strictly sequentially."*
3. **DO NOT PROMISE**: *"The Coordinator is forced by a code compiler to call both agents."*
4. **DO EXPLAIN**: *"The Coordinator dynamically reasons over the inquiry, decides which specialist tools are required, and orchestrates calls based on its PICOT decomposition plan."*

---

## 2. Observed Routing Characteristics

Based on live telemetry logs, integration testing, and Agent Studio Preview execution traces:

### Question 1: Does Coordinator always call Evidence Specialist?
- **Observed Behavior**: **YES**, for academic/clinical surgical inquiries.
- **Mechanism**: The Coordinator instructions explicitly mandate PICOT decomposition and delegation of scholarly research to the `evidence-specialist`. In all tested clinical questions (H1–H5), the Coordinator generated an explicit subagent call to `evidence-specialist`.
- **Exception**: In pure safety boundary refusals (e.g. Test H6), if the Coordinator halts immediately upon detecting an unsafe clinical dilemma, it may generate an immediate educational refusal without invoking the literature specialist.

### Question 2: Does Coordinator always call Guideline Specialist?
- **Observed Behavior**: **YES**, for comprehensive inquiries asking about societal consensus, standard of care, or clinical guidelines.
- **Mechanism**: System instructions direct the Coordinator to query professional surgical societies via `guideline-specialist`.
- **Variation**: If a user prompt asks purely about in vitro bench science or a pure animal model with no clinical human context, the Coordinator might prioritize literature over guidelines. However, for workshop demo questions, both are invoked.

### Question 3: Can they execute in different orders?
- **Observed Behavior**: **YES**.
- **Explanation**: In trace logs, `evidence-specialist` is frequently called first because the Coordinator prompt enumerates the literature task before the guideline task in Step 1. However, the model is an autonomous planner. Depending on prompt phrasing (e.g., *"What do SAGES guidelines say about ICG, and what clinical trials support this?"*), the model may invoke `guideline-specialist` before `evidence-specialist`.

### Question 4: Can they execute in parallel?
- **Observed Behavior**: **DEPENDS ON RUNTIME ENVIRONMENT**.
- **In ADK**: ADK's single-turn subagent execution loop dispatches subagent tool calls dynamically. When the model emits multiple subagent calls in a single turn, the runtime can resolve them asynchronously.
- **In Agent Studio Preview**: The visual canvas trace shows sequential progress bars as each subagent processes and returns its grounding results. True backend parallelism depends on platform request scheduling, but users experience the aggregate workflow as a continuous multi-step progression.

### Question 5: Is delegation dependent on prompt wording?
- **Observed Behavior**: **YES**.
- **Explanation**: Highly structured prompts matching the PICOT pattern trigger clean, rapid dual-specialist delegation. Conversational or ambiguous prompts require the Coordinator to perform additional reasoning turns to infer the missing parameters before delegating.

### Question 6: Can Coordinator answer without calling specialists?
- **Observed Behavior**: **YES, IN SPECIFIC SCENARIOS**:
  1. *Immediate Safety Refusal*: When prompted with explicit patient clinical vignettes (e.g., patient age, scheduled surgery date, individual treatment go/no-go dilemma), the Coordinator can trigger the safety refusal directly without invoking specialists.
  2. *Defective Prompting*: If the Coordinator prompt did not mandate delegation, a standard LLM might attempt to answer from parametric memory. Our instructions prevent this by mandating: *"You have ONLY access to the evidence-specialist and guideline-specialist subagents. Synthesize findings directly from subagent responses."*

---

## 3. Recommended Workshop Narrative for Presenters

When presenting the live demo (Minutes 20–25), presenters should use the following verified phrasing:

> *"Notice how the Coordinator Agent acts as an autonomous clinical orchestrator. Rather than following a rigid, brittle hard-coded script, it interprets the surgical research question, performs a PICOT breakdown, and dynamically invokes the Evidence Specialist and Guideline Specialist.*
> 
> *In our trace panel here, you can see the Coordinator issuing sub-queries, the subagents executing Google Search grounding in the background, and the findings returning to the Coordinator for cross-specialist synthesis. This flexibility is what distinguishes an agentic architecture from traditional rule-based workflow automation."*
