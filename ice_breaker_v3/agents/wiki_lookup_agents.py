from langchain.agents import initialize_agent, Tool, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import get_search_url


def lookup(name: str) -> str:
    """LangChain agent that finds a Wikipedia URL for a given person."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    tools_for_agent = [
        Tool(
            name="Crawl Google Wikipedia for person detail",
            func=get_search_url,
            description="Useful for getting a person's Wikipedia URL.",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,  # ✅ Pass LLM here
        verbose=True,
    )

    wikipedia_search_url = agent.run(name)
    return wikipedia_search_url
