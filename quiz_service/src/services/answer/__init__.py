from abc import ABC, abstractmethod
from src.models.question import QuestionLocalization
from typing import Dict, Protocol

class IAnswerChecker(Protocol):
    @abstractmethod
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool: ...