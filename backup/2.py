from functools import cached_property

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import Client
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context



class GlobalGemini(Gemini):
  """Pins the Vertex AI client to the `global` location.

  gemini-3 series models are only served from `global`; the default ADK
  `Gemini` integration constructs a `google.genai.Client` whose location
  defaults to the AgentEngine instance's region (e.g. `us-central1`) and
  fails with model-not-found for these models. Subclassing per the override
  pattern documented on `google.adk.models.google_llm.Gemini` lets the agent
  keep running in its regional AgentEngine instance while routing the model
  request to the global endpoint.
  """

  @cached_property
  def api_client(self) -> Client:
    return Client(vertexai=True, location="global")


final_writer = LlmAgent(
  name='final_writer',
  model='gemini-2.5-flash',
  description=(
      'STEP 6. Synthesizes balanced findings strictly using verified sources and calibrated language.'
  ),
  sub_agents=[],
  instruction='You are the Final Writer, the final step in the surgical research chain. Synthesize all findings into a balanced, rigorous report for the user.\n\nStrict Evidence Integrity Rules:\n1. Only use sources marked \'Status: Verified\' to support clinical and guideline claims. If a source failed verification, mark it under limitations as \'Source verification failed\' and do not cite it as evidence.\n2. Clearly distinguish guideline recommendations from meta-analyses and individual RCTs.\n3. Use calibrated, measured language. Never use overconfident phrases such as \'consistently proves\' or \'definitively reduces\'. Prefer nuanced phrasing (e.g., \'Recent meta-analyses generally report lower leak rates...\').\n\nStructure your reply:\n- Bottom line\n- Key evidence (verified trials and meta-analyses)\n- Guideline (verified professional guidance)\n- Recent evidence (verified publications from the last 2 years)\n- Main limitation (heterogeneity, unverified sources, or residual uncertainty)\n- Sources (list complete verified URLs with their provenance)',
  tools=[],
)
source_checker_google_search_agent = LlmAgent(
  name='Source_Checker_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
source_checker_url_context_agent = LlmAgent(
  name='Source_Checker_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
source_checker = LlmAgent(
  name='source_checker',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'STEP 5. Verifies source URLs, checks title matches, and recovers missing URLs via search fallback.'
  ),
  sub_agents=[final_writer],
  instruction='You are the Source Checker, step 5 in the research chain. Verify the integrity and validity of all upstream sources.\n\nRules:\n1. Never ask the user for URLs. Never guess PubMed IDs, DOIs, or URL patterns.\n2. For each source, check whether the reported URL exists and use URL Context to check if the resolved article title matches the claimed title.\n3. If the URL is missing, invalid, or points to an unrelated paper, use Google Search with the exact article title to find the legitimate URL.\n4. If a valid match is recovered via search, verify its content and set provenance to \'RECOVERED_BY_SEARCH\'. If no match can be confirmed, mark status as \'Source not found\'.\n\nFor each source, output:\nSource:\nClaimed title:\nOriginal URL supplied by upstream:\nVerified URL:\nStatus: [Verified / Invalid URL / Source not found / Missing URL]\nURL provenance: [DIRECT_SEARCH_RESULT / UPSTREAM_AGENT / RECOVERED_BY_SEARCH / NOT_AVAILABLE]\nReason: [Short explanation of match or mismatch]\n\nDelegate all verification outputs and cumulative findings to the **Final Writer** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=source_checker_google_search_agent),
    agent_tool.AgentTool(agent=source_checker_url_context_agent)
  ],
)
study_critic_google_search_agent = LlmAgent(
  name='Study_Critic_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
study_critic_url_context_agent = LlmAgent(
  name='Study_Critic_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
study_critic = LlmAgent(
  name='study_critic',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'STEP 4. Evaluates evidence consistency, study limitations, and clinical uncertainty.'
  ),
  sub_agents=[source_checker],
  instruction='You are the Study Critic, step 4 in the research chain. Review all cumulative findings from the previous research agents. Evaluate study consistency, methodological quality, study heterogeneity, and clinical uncertainty. Summarize 3 to 5 concise critique points. Delegate all cumulative findings, critique points, and source URLs to the **Source Checker** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=study_critic_google_search_agent),
    agent_tool.AgentTool(agent=study_critic_url_context_agent)
  ],
)
recent_evidence_finder_google_search_agent = LlmAgent(
  name='Recent_Evidence_Finder_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
recent_evidence_finder_url_context_agent = LlmAgent(
  name='Recent_Evidence_Finder_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
recent_evidence_finder = LlmAgent(
  name='recent_evidence_finder',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'STEP 3. Finds recent surgical literature from the last 2 years with strict URL verification.'
  ),
  sub_agents=[study_critic],
  instruction='You are the Recent Evidence Finder, step 3 in the research chain. Review cumulative findings and search specifically for surgical evidence published in the last 2 years using Google Search.\n\nNever fabricate or guess URLs. Only report URLs directly returned by the search tool. If not available, write \'NOT_AVAILABLE\'.\n\nFor each recent source, return:\n- Title: [Exact title]\n- Study type: [Study type]\n- Recent update: [What this adds to prior literature]\n- Search result URL: [https://... or NOT_AVAILABLE]\n- URL provenance: [DIRECT_SEARCH_RESULT or NOT_AVAILABLE]\n\nDelegate all cumulative findings to the **Study Critic** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=recent_evidence_finder_google_search_agent),
    agent_tool.AgentTool(agent=recent_evidence_finder_url_context_agent)
  ],
)
guideline_finder_google_search_agent = LlmAgent(
  name='Guideline_Finder_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
guideline_finder_url_context_agent = LlmAgent(
  name='Guideline_Finder_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
guideline_finder = LlmAgent(
  name='guideline_finder',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'STEP 2. Finds surgical society guidelines with strict search-result URL provenance.'
  ),
  sub_agents=[recent_evidence_finder],
  instruction='You are the Guideline Finder, step 2 in the research chain. Review the findings from Evidence Finder and search for relevant surgical guidelines or consensus statements from major societies using Google Search.\n\nNever invent, guess, or derive URLs from memory or society names. Copy the exact URL returned by the search tool. If the search tool does not return an accessible URL, write \'NOT_AVAILABLE\'.\n\nFor each guideline, return:\n- Organization: [Society name]\n- Recommendation or position: [Position statement]\n- Evidence strength: [If reported]\n- Search result URL: [https://... or NOT_AVAILABLE]\n- URL provenance: [DIRECT_SEARCH_RESULT or NOT_AVAILABLE]\n\nDelegate all cumulative findings to the **Recent Evidence Finder** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=guideline_finder_google_search_agent),
    agent_tool.AgentTool(agent=guideline_finder_url_context_agent)
  ],
)
evidence_finder_google_search_agent = LlmAgent(
  name='Evidence_Finder_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
evidence_finder_url_context_agent = LlmAgent(
  name='Evidence_Finder_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
evidence_finder = LlmAgent(
  name='evidence_finder',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'STEP 1. Finds clinical evidence with strict URL provenance and no fabricated links.'
  ),
  sub_agents=[guideline_finder],
  instruction='You are the Evidence Finder, step 1 in the research chain. Find up to 3 strong clinical studies, systematic reviews, or meta-analyses answering the question using Google Search.\n\nNever invent, reconstruct, guess, or manually generate a URL from memory, title, DOI, or PubMed ID. Only report a URL that was directly returned by the search tool. Copy the URL exactly as returned. If no URL is returned, report \'NOT_AVAILABLE\'.\n\nFor every source, format as:\n- Title: [Exact title]\n- Year: [Publication year]\n- Study type: [RCT / Systematic review / Meta-analysis]\n- Finding: [Concise clinical finding]\n- Search result URL: [https://... or NOT_AVAILABLE]\n- URL provenance: [DIRECT_SEARCH_RESULT or NOT_AVAILABLE]\n\nDelegate all findings and the original question to the **Guideline Finder** sub-agent.',
  tools=[
    agent_tool.AgentTool(agent=evidence_finder_google_search_agent),
    agent_tool.AgentTool(agent=evidence_finder_url_context_agent)
  ],
)
root_agent = LlmAgent(
  name='Surgical_Research_Coordinator',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Coordinates the surgical research workflow by starting the sequential agent chain.'
  ),
  sub_agents=[evidence_finder],
  instruction='You are the Surgical Research Coordinator. When the user asks a research question, delegate it directly to the **Evidence Finder** sub-agent to initiate the research pipeline. Do not attempt to answer directly or terminate early; allow the chain to proceed through all specialist agents until the Final Writer completes the synthesis.',
  tools=[],
)