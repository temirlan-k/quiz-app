import enum


class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    FILL_BLANK = "fill_blank"
    MULTIPLE_CHOICE = "multiple_choice"
    MATCHING = "matching"


class LanguageCode(str, enum.Enum):
    EN = "en"
    ES = "es"
    PT = "pt"
    DE = "de"
    TR = "tr"
    FR = "fr"
