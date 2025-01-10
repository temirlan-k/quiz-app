from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel


class AnswerRequest(BaseModel):
    session_id: UUID
    language_code: str
    answer_content: Dict[str, Any]

    class Config:
        schema_example = {
            {
                "session_id": "120184c6-5773-42aa-806a-75aa5f77fdba",
                "answer_content": {"selected_options": ["opt1"]},
            }
        }
