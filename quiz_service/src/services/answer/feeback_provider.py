from abc import ABC, abstractmethod

from src.core.enums import QuestionType
from src.models.question import QuestionLocalization


class IFeedbackProvider(ABC):
    @abstractmethod
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        pass


class SingleChoiceFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        private_data = question_l.content.get("private_data", {})
        public_data = question_l.content.get("public_data", {})

        correct_option_ids = private_data.get("correct_options", [])
        print(correct_option_ids)
        options = public_data.get("options", [])
        correct_options = [
            option["text"] for option in options if option["id"] in correct_option_ids
        ]
        return f"Wrong! Correct option(s): {', '.join(correct_options)} "


class MultipleChoiceFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        private_data = question_l.content.get("private_data", {})
        public_data = question_l.content.get("public_data", {})


        correct_options = private_data.get(
            "correct_options", []
        )
        options = public_data.get("options", [])
        correct_options = [
            option["text"] for option in options if option["id"] in correct_options
        ]
        return f"Wrong! Correct option(s): {', '.join(correct_options)}"


class FillBlankFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        private_data = question_l.content.get("private_data", {})
        public_data = question_l.content.get("public_data", {})
        correct_options = private_data.get('correct_answers')
        options = public_data.get('options')
        correct_values = [
          option  for option in options if option in correct_options
        ]
        return f"Wrong! Correct answer(s): {', '.join(correct_values)}"


class MatchingFeedbackProvider(IFeedbackProvider):
    def generate_feedback(self, question_l: QuestionLocalization) -> str:
        correct_pairs = question_l.content.get("private_data", {}).get("pairs", [])
        formatted_pairs = "; ".join(
            f"{p['left']} -> {p['right']}" for p in correct_pairs
        )
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
        if not provider:
            raise ValueError(f"No feedback provider for question type: {question_type}")
        return provider
