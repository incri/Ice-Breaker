import os
from dotenv import load_dotenv
from wikipedia_scraper import get_wikipedia_data
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.wiki_lookup_agents import lookup

# Load environment variables
load_dotenv()

# Ensure API keys are set
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
    raise ValueError(
        "❌ Missing API keys! Set GOOGLE_API_KEY and SERPAPI_API_KEY in .env."
    )


# 🧠 Generate AI-based Summary
def generate_summary(person_name: str):
    """Fetch Wikipedia data and generate a summary using Gemini AI."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    summary_template = """
        Given the following Wikipedia information about {person_name}, create:
        1. A short summary.
        2. Two interesting facts about them.

        Wikipedia Info:
        {information}
    """

    summary_prompt = PromptTemplate(
        input_variables=["person_name", "information"], template=summary_template
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

    return {
        "person": person_name,
        "summary": result,
        "image": wiki_data["thumbnail"],
    }


if __name__ == "__main__":
    person = "Donald Trump"

    print("🔍 Searching for Wikipedia URL...")
    wikipedia_url = lookup(person)
    print(f"✅ Found Wikipedia URL: {wikipedia_url}")

    print("\n📄 Fetching Wikipedia Data...")
    wiki_data = get_wikipedia_data(person)
    print(f"📝 Wikipedia Summary: {wiki_data['summary'][:300]}...")

    print("\n🧠 Generating AI-based Summary...")
    final_summary = generate_summary(person)
    print(f"\n🎯 Final Summary:\n{final_summary}")
