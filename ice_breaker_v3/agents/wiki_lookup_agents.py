from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_search_url


def lookup(name: str) -> str:

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    template = """given the full name {name_of_person} I want you to get it me a link to their wiki search deatil page.
                your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl Google wikipedia for person detail",
            func=get_search_url,
            description="Useful for when you need to get detail about people wikipedia URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    wikipedia_search_url = agent.run(prompt_template.format_prompt(name_of_person=name))

    return wikipedia_search_url
