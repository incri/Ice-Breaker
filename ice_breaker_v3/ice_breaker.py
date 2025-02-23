import os
from dotenv import load_dotenv
from wikipedia_scraper import get_wikipedia_data
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.wiki_lookup_agents import lookup
from output_parsers import person_intel_perser

# Load environment variables
load_dotenv()

# Ensure API keys are set
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
    raise ValueError(
        "❌ Missing API keys! Set GOOGLE_API_KEY and SERPAPI_API_KEY in .env."
    )


def generate_summary(person_name: str):
    """Fetch Wikipedia data and generate a summary using Gemini AI."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    summary_template = """
        Given the following Wikipedia information  Wikipedia Info: {information} about {person_name}, create:
        1. A short summary.
        2. Two interesting facts about them.
        3. Two topic that may intrest them.
        4. Two creative Ice breakers to open a coversations with them.

       \n{format_instructions}


    """

    summary_prompt = PromptTemplate(
        input_variables=["person_name", "information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_perser.get_format_instructions()
        },
    )

    # Fetch Wikipedia data
    wiki_data = get_wikipedia_data(person_name)

    if "error" in wiki_data:
        return wiki_data["error"]

    # Generate response using Gemini
    response = summary_prompt | llm
    result = response.invoke(
        {"person_name": person_name, "information": wiki_data["summary"]}
    )

    # Format output as plain text
    return f"Summary of {person_name}:\n\n{result.content}"


if __name__ == "__main__":
    person = "Donald Trump"
    final_summary = generate_summary(person)
    print(final_summary)
