from typing import List

from pydantic import BaseModel

from src.core.enums import LanguageCode


class QuizLocalization(BaseModel):
    language: LanguageCode
    title: str
    description: str


class QuizCreateRequest(BaseModel):
    localizations: List[QuizLocalization]
