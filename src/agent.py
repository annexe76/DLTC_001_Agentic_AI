from typing import Dict, List, Any, Callable
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain.schema import AIMessage, HumanMessage

class ExplanationRequest(BaseModel):
  """Request for an explanation of a CPS230 section."""
  section: str = Field(description="The section of CPS230 to be explained")

class ImplementationRequest(BaseModel):
  """Request for implementation steps for a CPS230 section."""
  section: str = Field(description="The section of CPS230 for which implementation steps are needed")

class CPS230Agent:
  def __init__(self, vectorestore):
    """Initialising the CPS230 agent."""
    self.vectorstore = vectorstore
    self.llm = ChatOpenAI(model="gpt-4" temperature=0)
    
    # Set up agent with tools
    self.tools = [
        self.explain_section,
        self.provide_implementation_steps,
        self.search_related_content
    ]

    self.functions = [format_tool_to_openai_function(t) for t in self.tools]

    # Create the promp template
    self.prompt = ChatPromptTemplate.from_message([
      ("system","""You are a helpful assistant specialised in APRA CPS230 regulations.
      You help users understand the APRA CPS230 prudential standard on Operational Risk Management 
      and provide guidance on implementing its requirements.
      
      Your responses should be clear, accurate and helpful. When explaining sections,
      use plain English that is accessible to non-speacialists. When providing implementation steps,
      be specific and actionable for an australian banking institution.
      
      If you're unsure about something, acknowledge it and provide the best guidance you can based on
      the availabile information."""),
      MessagesPlaceholder(variable_name="chat_history"),
      ("human","{input}"),
      MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Build the agent
    self.agent = (
        {
            "input": lambda x: x["input"],
            "chat_history": lambda x: x.get("chat_history", []),
            "agent_scratchpad": lambda x: format_to_openai_function_message(x["intermediate_steps"]),
        }
        | self.prompt
        | self.llm.bind(functions=self.functions)
        | OpenAIFunctionsAgentOutputParser()
    )

  @tool(args_schema=ExplanationRequest)
  def explain_section(self, section: str) -> str:
    """Explain a specific section of CPS230 in plain English."""
    query = f"Explain section {section} of CPS230"
    docs = self.vectorstore.query(query)

    if not docs:
        return "I couldn't find specific information about this section."

    context = "\n\n".join([doc.page_content for doc in docs])

    prmpt = f"""
    Based on the following context from CPS230, explain section {section} in plain English
    that would be understanble to someone without a regulatory backgorund:

    {context}

    Explanation in plain English:
    """

    messages = [HumanMessage(content=prompt)]
    response = self.llm.invoke(messages)
    return response.content

  @tool(args_schema=ImplementationRequest)
  def provide_implementation_steps(self, section: str) -> str:
    """Provide implementation steps for a specific section of CPS230."""
      query = f"Implementation steps for section {section} of CPS230"
      docs = self.vectorstore.query(query)

      if not docs:
          return "I couldn't find specific information about implementing this section."

      context = "\n\n".join([doc.page_content for doc in docs])

      prompt = f"""
      Based on the following context from CPS230, provide clear, practical steps to implement the requirements in section {section}:

      {context}

      Implementation steps (provide numbered steps):
      """

      message = [HumanMessage(content=prompt)]
      response = self.llm.invoke(message)
      return response.content
  
  @tool
  def search_related_content(self, query: str) -> str:
    """Search for content in CPS230 related to a specific query."""
    docs = self.vectorstore.query(query, k=3)

    if not docs:
      return "I couldn't find information related to this query."

    return "\n\n".join([f"From section {doc.metadata.get('section', 'unknown')}:\n{doc.page_content}"
                        for doc in docs])

  def run(self, query: str, chat_history: List = None):
    """Run the agent on a query."""
    if chat_history is None:
      chat_history = []

    return = self.agent.invoke({
      "input": query,
      "chat_history": chat_history,
      "intermediate_steps": []
    })

    return result
