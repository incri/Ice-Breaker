import os
from dotenv import load_dotenv
from wikipedia_scraper import get_wikipedia_data
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.wiki_lookup_agents import lookup
from output_parsers import person_intel_perser, PersonIntel
from typing import Tuple

# Load environment variables
load_dotenv()

# Ensure API keys are set
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
    raise ValueError(
        "❌ Missing API keys! Set GOOGLE_API_KEY and SERPAPI_API_KEY in .env."
    )


def generate_summary(person_name: str) -> Tuple[PersonIntel, str]:
    """Fetch Wikipedia data and generate a summary using Gemini AI."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    summary_template = """
        Given the following Wikipedia information about {person_name}:
        {information}

        Create a structured JSON response containing:
        - A short summary.
        - Two interesting facts about them.
        - Two topics that may interest them.
        - Two creative icebreakers to start a conversation.

        Respond **ONLY** in valid JSON format without Markdown or code block formatting.

        {format_instructions}
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
    thumbnail_url = wiki_data.get("thumbnail")

    if "error" in wiki_data:
        return wiki_data["error"]

    # Generate response using Gemini
    response = summary_prompt | llm
    result = response.invoke(
        {"person_name": person_name, "information": wiki_data["summary"]}
    )

    try:
        # Ensure proper JSON parsing using the output parser
        parsed_result = person_intel_perser.parse(result.content)
    except Exception as e:
        raise ValueError(
            f"❌ Failed to parse response: {e}\nResponse: {result.content}"
        )

    return parsed_result, thumbnail_url
