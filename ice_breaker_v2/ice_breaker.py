import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from wikipedia_scraper import get_wikipedia_data


# Load environment variables from .env file
load_dotenv()

# Ensure the GOOGLE_API_KEY is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ Missing GOOGLE_API_KEY! Please set it in your environment.")

information = get_wikipedia_data("Albert Einstein")

if __name__ == "__main__":
    print("Hello Google Gemini!")

    # Define the prompt template
    summary_template = """
        Given the Person information {information} about a person, create:
        1. A short summary.
        2. Two interesting facts about them.
    """

    # Create the PromptTemplate
    summary_prompt = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # Initialize the ChatGoogleGenerativeAI model
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    # Create a runnable sequence
    response = summary_prompt | llm

    # Invoke the sequence with the provided information
    result = response.invoke({"information": information})

    print(result)
