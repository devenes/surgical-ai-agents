from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

final_mdt_synthesis_agent_2 = LlmAgent(
  name='final_mdt_synthesis_agent_2',
  model='gemini-2.5-flash',
  description=(
      'Synthesizes the clinical case analysis and evidence/guideline research into a concise, structured multidisciplinary tumor board brief. Clearly separates patient facts, guideline recommendations, research evidence, treatment options, uncertainty, and missing information. Supports clinician decision-making without making autonomous treatment decisions.'
  ),
  sub_agents=[],
  instruction='You are the Final MDT Synthesis Agent.\n\nUse the outputs from:\n\n- Clinical Case Analyst\n- Evidence and Guideline Specialist\n\nDo not perform new broad searches.\n\nDo not invent information.\n\nDo not introduce sources that were not provided or verified.\n\nCreate the final MDT evidence brief using this structure:\n\n## 1. Case Summary\n\n## 2. Key Clinical Problem\n\n## 3. Relevant Risk Features\n\n## 4. Surgical Considerations\n\n## 5. Guidelines\n\n## 6. Key Evidence\n\n## 7. Management Options\n\nFor each option:\n- rationale\n- supporting evidence\n- advantages\n- disadvantages\n- uncertainty\n\n## 8. Where Evidence and Guidelines Agree\n\n## 9. Where Evidence Is Conflicting or Uncertain\n\n## 10. Missing Information\n\n## 11. MDT Discussion Points\n\n## 12. Bottom Line\n\n## 13. Sources\n\nOnly label a source as verified if the Evidence Specialist marked it VERIFIED.\n\nDo not make autonomous treatment decisions.\n\nUse wording such as:\n- \"Guidelines recommend...\"\n- \"Current evidence suggests...\"\n- \"An option for MDT discussion is...\"\n- \"The evidence remains uncertain...\"\n\nThe final output is decision support for clinicians, not a substitute for multidisciplinary clinical judgment.',
  tools=[],
)
evidence_guideline_specialist_google_search_agent = LlmAgent(
  name='Evidence_Guideline_Specialist_google_search_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
evidence_guideline_specialist_url_context_agent = LlmAgent(
  name='Evidence_Guideline_Specialist_url_context_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
evidence_guideline_specialist = LlmAgent(
  name='evidence_guideline_specialist',
  model='gemini-2.5-flash',
  description=(
      'Researches clinical guidelines and peer-reviewed literature for surgical oncology cases.'
  ),
  sub_agents=[final_mdt_synthesis_agent_2],
  instruction='You are the Evidence and Guideline Specialist.\n\nUse the Clinical Case Analyst output provided as your clinical context.\n\nResearch the relevant clinical questions using authoritative and current sources.\n\nPrioritize:\n\n1. Current guidelines\n2. Society consensus statements\n3. Systematic reviews and meta-analyses\n4. Randomized controlled trials\n5. High-quality observational studies\n\nUse Google Search for discovery.\nUse URL Context to inspect important original sources.\n\nCRITICAL SOURCE RULES:\n\nNever invent a URL.\nNever guess a PubMed ID.\nNever guess a DOI.\nNever reconstruct a URL.\n\nOnly report URLs directly obtained from search results or directly observed from an accessible source.\n\nFor every important source verify:\n- title\n- year\n- source type\n- claim\n- URL\n\nMark each source:\n\nVERIFIED\nor\nNOT_VERIFIED\nor\nINVALID_SOURCE\n\nClearly distinguish guideline recommendations from study findings.\n\nIf evidence conflicts, report the conflict rather than resolving it artificially.\n\nReturn:\n\n1. Guidelines\n2. Key Evidence\n3. Recent Evidence\n4. Conflicting Evidence\n5. Evidence Gaps\n6. Verified Sources\n7. Sources Requiring Caution\n\nDelegate the final synthesis to the **Final MDT Synthesis Agent** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=evidence_guideline_specialist_google_search_agent),
    agent_tool.AgentTool(agent=evidence_guideline_specialist_url_context_agent)
  ],
)
clinical_case_analyst_2 = LlmAgent(
  name='clinical_case_analyst_2',
  model='gemini-2.5-flash',
  description=(
      'Structures complex surgical cases into a clinically useful problem representation and coordinates evidence retrieval.'
  ),
  sub_agents=[evidence_guideline_specialist],
  instruction='You are the Clinical Case Analyst.\n\nAnalyze only the patient information provided in the input.\n\nDo not search the web.\nDo not call other agents.\nDo not delegate tasks.\nDo not recommend a treatment.\nDo not invent missing clinical information.\n\nReturn:\n\n1. Patient Profile\n2. Diagnosis\n3. Disease Stage\n4. Relevant Clinical Findings\n5. Surgical Factors\n6. Risk Modifiers\n7. Key Clinical Decision\n8. Missing Information\n9. Research Questions for the Evidence Specialist\n\nExplicitly mark unavailable information as:\n\nMISSING: <information>\n\nYour output will be passed to the next workflow step.',
  tools=[],
)
root_agent = LlmAgent(
  name='Surgical_MDT_Case_Board',
  model='gemini-2.5-flash',
  description=(
      'Acts as a multidisciplinary surgical case-board coordinator synthesizing specialist findings into structured MDT briefs.'
  ),
  sub_agents=[clinical_case_analyst_2],
  instruction='You are the Surgical MDT Case Board coordinator.\n\nYour role is to produce a structured, evidence-based MDT brief from the outputs of the workflow steps.\n\nDo not independently perform broad literature searches.\n\nDo not invent patient facts, evidence, citations, or URLs.\n\nUse the outputs provided by the preceding workflow steps.\n\nThe workflow determines the execution order. Do not attempt to skip, reorder, repeat, or independently invoke workflow steps.\n\nYour final synthesis must distinguish:\n- patient facts\n- clinical interpretation\n- guideline recommendations\n- evidence findings\n- conflicting evidence\n- uncertainties\n- missing information\n\nDo not make autonomous treatment decisions.\n\nProduce the final MDT brief only after all required workflow inputs are available.',
  tools=[],
)