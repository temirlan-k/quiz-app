from abc import ABC, abstractmethod
from typing import Dict, Protocol

from src.models.question import QuestionLocalization


class IAnswerChecker(Protocol):
    @abstractmethod
    def check_answer(
        self, question_l: QuestionLocalization, user_answer_data: Dict
    ) -> bool: ...
