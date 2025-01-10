import enum


class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    FILL_BLANK = "FILL_BLANK"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    MATCHING = "MATCHING"


class LanguageCode(str, enum.Enum):
    EN = "en"
    ES = "es"
    PT = "pt"
    DE = "de"
    TR = "tr"
    FR = "fr"


class EventType(str,enum.Enum):
    QUIZ_COMPLETED = "QUIZ_COMPLETED"
