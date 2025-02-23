from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class PersonIntel(BaseModel):
    summary: str = Field(description="summary of a person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interest: List[str] = Field(
        description="Topics that may intrest the person"
    )
    ice_breakers: List[str] = Field(
        description="create ice breakers to open a conversation with the person"
    )

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topic_of_interest": self.topics_of_interest,
            "ice_breaker": self.ice_breakers,
        }


person_intel_perser = PydanticOutputParser(pydantic_object=PersonIntel)
