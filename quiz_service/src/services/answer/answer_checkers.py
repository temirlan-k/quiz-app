from typing import Dict
from uuid import UUID
from abc import ABC, abstractmethod
from src.models.question import QuestionLocalization
from src.core.enums import QuestionType

class IAnswerChecker(ABC):
    @abstractmethod
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool: ...

class SingleChoiceChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_options = question_l.content.get("private_data", {}).get("correct_options", [])
        user_option = user_answer_data.get("selected_option")
        return user_option in correct_options

class FillBlankChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_answers_lists = question_l.content.get("private_data", {}).get("correct_answers", [])
        user_answers = user_answer_data.get("answers", [])
        normalized_user = [str(ans).strip().lower() for ans in user_answers]
        
        for correct_set in correct_answers_lists:
            if not isinstance(correct_set, list):
                correct_set = [correct_set]
            normalized_db_correct = [str(ans).strip().lower() for ans in correct_set]
            if normalized_db_correct == normalized_user:
                return True
        return False

class MultipleChoiceChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_options = question_l.content.get("private_data", {}).get("correct_options", [])
        user_selected = user_answer_data.get("selected_options", [])
        normalized_user = set(str(opt).strip().lower() for opt in user_selected)
        normalized_db_correct = set(str(opt).strip().lower() for opt in correct_options)
        return normalized_user == normalized_db_correct

class MatchingChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_pairs = question_l.content.get("private_data", {}).get("pairs", [])
        user_matches = user_answer_data.get("matches", [])
        return self._normalize_pairs(correct_pairs) == self._normalize_pairs(user_matches)

    def _normalize_pairs(self, pairs):
        return { (str(p.get("left")).strip().lower(), str(p.get("right")).strip().lower()) for p in pairs }

class AnswerCheckerFactory:
    _checkers = {
        QuestionType.SINGLE_CHOICE: SingleChoiceChecker(),
        QuestionType.FILL_BLANK: FillBlankChecker(),
        QuestionType.MULTIPLE_CHOICE: MultipleChoiceChecker(),
        QuestionType.MATCHING: MatchingChecker(),
    }

    @classmethod
    def get_checker(cls, question_type: QuestionType) -> IAnswerChecker:
        if question_type not in cls._checkers:
            raise ValueError(f"No checker found for {question_type}")
        return cls._checkers[question_type]
