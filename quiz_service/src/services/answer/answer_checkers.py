from typing import Dict
from uuid import UUID
from abc import ABC, abstractmethod
from src.core.exceptions.base import BadRequestException
from src.models.question import QuestionLocalization
from src.core.enums import QuestionType

class IAnswerChecker(ABC):
    @abstractmethod
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool: ...

class SingleChoiceChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_options = question_l.content.get("private_data", {}).get("correct_options", [])
        user_option = user_answer_data.get("selected_option")
        print(correct_options)
        return user_option == correct_options

class FillBlankChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_answers_lists = question_l.content.get("private_data", {}).get("correct_answers", [])
        user_answers = user_answer_data.get("selected_option", [])
        normalized_user = [str(ans).strip().lower() for ans in user_answers]
        normalized_db_correct = [str(ans).strip().lower() for ans in correct_answers_lists]
        if normalized_db_correct == normalized_user:
            return True
        return False

class MultipleChoiceChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        correct_options = question_l.content.get("private_data", {}).get("correct_options", [])
        print(correct_options)
        user_selected = user_answer_data.get("selected_option", [])
        print(user_selected)
        normalized_user = set(str(opt).strip().lower() for opt in user_selected)
        normalized_db_correct = set(str(opt).strip().lower() for opt in correct_options)
        print(normalized_db_correct,normalized_user)
        if (normalized_db_correct) == (normalized_user):
            return True
        return False

class MatchingChecker(IAnswerChecker):
    def check_answer(self, question_l: QuestionLocalization, user_answer_data: Dict) -> bool:
        try:
            correct_pairs = question_l.content.get("private_data", {}).get("pairs", [])
            user_matches = user_answer_data.get("selected_option").get("matches", [])
            if not user_matches or len(user_matches)!=len(correct_pairs):   
                raise BadRequestException("You should match all pairs")
            print("CORRECT",correct_pairs)
            print("USER",user_matches)
            print(user_matches is correct_pairs)
            return self._normalize_pairs(user_matches) == self._normalize_pairs(correct_pairs)
        except Exception as e:
            raise BadRequestException("INTERNAL")

    def _normalize_pairs(self,pairs):
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
