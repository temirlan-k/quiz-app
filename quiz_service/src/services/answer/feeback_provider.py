# src/services/feedback_providers.py
from abc import ABC, abstractmethod
from typing import Dict
from src.models.question import QuestionLocalization
from src.core.enums import QuestionType

class IFeedbackProvider(ABC):
    @abstractmethod
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        pass

class SingleChoiceFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        private_data = question_l.content.get("private_data", {})
        public_data = question_l.content.get("public_data", {})
        
        correct_option_ids = private_data.get("correct_options", [])
        
        options = public_data.get("options", [])
        correct_options = [
            option["text"] for option in options if option["id"] in correct_option_ids
        ]
        return f"Wrong! Correct option(s): {', '.join(correct_options)} "

class MultipleChoiceFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        correct_options = question_l.content.get("private_data", {}).get("correct_options", [])
        return f"Wrong! Correct option(s): {', '.join(correct_options)}"

class FillBlankFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        correct_answers = question_l.content.get("private_data", {}).get("correct_answers", [])
        return f"Wrong! Correct answer(s): {', '.join(correct_answers)}"

class MatchingFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        correct_pairs = question_l.content.get("private_data", {}).get("pairs", [])
        formatted_pairs = "; ".join(f"{p['left']} -> {p['right']}" for p in correct_pairs)
        return f"Wrong! Correct pairs: {formatted_pairs}"

class FeedbackProviderFactory:
    _providers = {
        QuestionType.SINGLE_CHOICE: SingleChoiceFeedbackProvider(),
        QuestionType.MULTIPLE_CHOICE: MultipleChoiceFeedbackProvider(),
        QuestionType.FILL_BLANK: FillBlankFeedbackProvider(),
        QuestionType.MATCHING: MatchingFeedbackProvider(),
    }

    @classmethod
    def get_provider(cls, question_type: QuestionType) -> IFeedbackProvider:
        provider = cls._providers.get(question_type)
        print(provider)
        if not provider:
            raise ValueError(f"No feedback provider for question type: {question_type}")
        return provider
