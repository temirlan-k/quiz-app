from typing import Dict, List, Union
from pydantic import UUID4, BaseModel
from src.core.enums import LanguageCode, QuestionType
from typing import List, Dict, Union
from pydantic import BaseModel, UUID4
from src.core.enums import LanguageCode, QuestionType


class MultipleChoiceContent(BaseModel):
    public_data: List[str]
    private_data: Dict


class SingleChoiceContent(BaseModel):
    public_data: List[str]
    private_data: Dict


class MatchingContent(BaseModel):
    public_data: Dict[str, List[str]]
    private_data: Dict


class FillInTheBlanksContent(BaseModel):
    public_data: List[str]
    private_data: Dict


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

    class Config:
        json_schema_extra = {
            "example": {
                "question_type": "MATCHING",
                "localizations": [
                    {
                        "language": "en",
                        "question_text": "What is 2+2?",
                        "content": {
                            "public_data": {
                                "shuffled_left": ["len", "sorted", "type"],
                                "shuffled_right": [
                                    "Devuelve el número de elementos en un objeto",
                                    "Devuelve una lista ordenada",
                                    "Devuelve el tipo de un objeto",
                                ],
                            },
                            "private_data": {
                                "pairs": [
                                    {
                                        "left": "len",
                                        "right": "Devuelve el número de elementos en un objeto",
                                    },
                                    {
                                        "left": "sorted",
                                        "right": "Devuelve una lista ordenada",
                                    },
                                    {
                                        "left": "type",
                                        "right": "Devuelve el tipo de un objeto",
                                    },
                                ]
                            },
                        },
                    }
                ],
            }
        }


class QuestionCreateRequest(BaseModel):
    question_type: QuestionType
    localizations: List[QuestionLocalization]

    class Config:
        json_schema_extra = {
            "example1": {
                "question_type": "EN",
                "content": {
                    "public_data": {
                        "shuffled_left": ["len", "sorted", "type"],
                        "shuffled_right": [
                            "Devuelve el número de elementos en un objeto",
                            "Devuelve una lista ordenada",
                            "Devuelve el tipo de un objeto",
                        ],
                    },
                    "private_data": {
                        "pairs": [
                            {
                                "left": "len",
                                "right": "Devuelve el número de elementos en un objeto",
                            },
                            {"left": "sorted", "right": "Devuelve una lista ordenada"},
                            {"left": "type", "right": "Devuelve el tipo de un objeto"},
                        ]
                    },
                },
            }
        }


class SelectedOption(BaseModel):
    selected_option: List[str]


class AnswerQuestionStandard(BaseModel):
    session_id: UUID4
    answer_content: SelectedOption

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "120184c6-5773-42aa-806a-75aa5f77fdba",
                "answer_content": {"selected_option": ["opt1", "opt2"]},
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
        json_schema_extra = {
            "example": {
                "session_id": "120184c6-5773-42aa-806a-75aa5f77fdba",
                "answer_content": {
                    "selected_option": {
                        "matches": [
                            {"left": "Apple", "right": "Fruit"},
                            {"left": "Paris", "right": "Capital"},
                        ]
                    }
                },
            }
        }
