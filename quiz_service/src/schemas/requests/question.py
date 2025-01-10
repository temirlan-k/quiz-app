from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

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
