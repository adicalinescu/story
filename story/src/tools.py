from typing import Optional
from pydantic import BaseModel, Field


class DirectAnswer(BaseModel):
    """
    Intent Agent Answer
    """
    answer: str = Field(default="", description="contains the general conversation answer to the user prompt")


class WriterAnswer(BaseModel):
    """
    Used to answer with a story or general answer
    """
    story: Optional[str] = Field(default="", description="contains exclusively the story, no introduction or conclusion")
    general_answer: Optional[str] = Field(default="", description="contains the general answer if no story is provided")

    def to_list(self) -> list:
        return [{
            "story": self.story,
            "general_answer": self.general_answer
        }]

class CriticAnswer(BaseModel):
    """
    Story Critic Agent Answer
    """
    # story: str = Field(default="", description="contains the story to be reviewed")
    feedback: str = Field(default="", description="contains your feedback on the story, the reasons why the story is not compliant")
    story_ok: bool = Field(default="", description="True if you validated the story is correct, False otherwise")

    def to_list(self):
        return [{
            # "story": self.report.to_dict(),
            "feedback": self.feedback,
            "story_ok": self.story_ok,
        }]
