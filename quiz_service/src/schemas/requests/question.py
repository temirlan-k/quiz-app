from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import UUID4, BaseModel, Field

from src.core.enums import LanguageCode, QuestionType


class MultipleChoiceContent(BaseModel):
    answers: List[str]
    correct_answers: List[int]
    hint: Optional[str] = None


class SingleChoiceContent(BaseModel):
    answers: List[str]
    correct_answer: int
    hint: Optional[str] = None


class MatchingContent(BaseModel):
    left_items: List[str]
    right_items: List[str]
    correct_matches: dict
    hint: Optional[str] = None


class FillInTheBlanksContent(BaseModel):
    text: str
    correct_answers: List[str]
    hint: Optional[str] = None


QuestionContent = Union[
    MultipleChoiceContent, SingleChoiceContent, MatchingContent, FillInTheBlanksContent
]


class QuestionLocalization(BaseModel):
    language: LanguageCode
    question_text: str
    content: QuestionContent


class QuestionCreateRequest(BaseModel):
    question_type: QuestionType
    localizations: List[QuestionLocalization]

class SelectedOption(BaseModel):
    selected_option: List[str]  

class AnswerQuestionStandard(BaseModel):
    session_id: UUID4
    answer_content: SelectedOption  

    class Config:
            schema_extra = {
                "example": {
                    "session_id": "120184c6-5773-42aa-806a-75aa5f77fdba",
                    "answer_content": {
                        "selected_option": ["opt1", "opt2"]
                    }
                }
            }
class SelectedOption(BaseModel):
    matches: List[Dict[str, str]]

class MatchingSelectedOption(BaseModel):
    selected_option: SelectedOption

class AnswerQuestionMatching(BaseModel):
    session_id: UUID4
    answer_content: MatchingSelectedOption

    class Config:
        schema_extra = {
            "example": {
                "session_id": "120184c6-5773-42aa-806a-75aa5f77fdba",
                "answer_content": {
                    "selected_option": {
                        "matches": [
                            {"left": "Apple", "right": "Fruit"},
                            {"left": "Paris", "right": "Capital"}
                        ]
                    }
                }
            }
        }
