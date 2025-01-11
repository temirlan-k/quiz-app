import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return so.mapped_column(sa.DateTime, default=sa.func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return so.mapped_column(
            sa.DateTime,
            default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        )


Base = so.declarative_base()

from .question import Question, QuestionLocalization
from .quiz import Quiz, QuizLocalization
from .quiz_session import UserQuizSession
from .user_attempt import UserAttempt
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

# Константы для переиспользования
QUIZ_ID = "a3dfe514-f1cc-4852-a377-cfa7a2007084"
QUESTION_SINGLE_CHOICE_ID = "c1dfe514-f1cc-4852-a377-cfa7a2007084"
QUESTION_MULTIPLE_CHOICE_ID = "c2dfe514-f1cc-4852-a377-cfa7a2007084"
QUESTION_FILL_BLANK_ID = "c3dfe514-f1cc-4852-a377-cfa7a2007084"
QUESTION_MATCHING_ID = "c4dfe514-f1cc-4852-a377-cfa7a2007084"

# Подготовка контента для вопросов
QUESTION_CONTENTS = {
    "single_choice": {
        "public_data": {
            "options": [
                {"id": "opt1", "text": "6"},
                {"id": "opt2", "text": "8"},
                {"id": "opt3", "text": "9"}
            ]
        },
        "private_data": {
            "correct_options": ["opt2"]
        }
    },
    "multiple_choice": {
        "public_data": {
            "options": [
                {"id": "opt1", "text": "int"},
                {"id": "opt2", "text": "float"},
                {"id": "opt3", "text": "decimal"}
            ]
        },
        "private_data": {
            "correct_options": ["opt1", "opt2"]
        }
    },
    "fill_blank": {
        "public_data": {
            "options": ["def", "function", "lambda"]
        },
        "private_data": {
            "correct_answers": ["def"]
        }
    },
    "matching": {
        "en": {
            "public_data": {
                "shuffled_left": ["len", "sorted", "type"],
                "shuffled_right": [
                    "Returns the number of items in an object",
                    "Returns a sorted list",
                    "Returns the type of an object"
                ]
            },
            "private_data": {
                "pairs": [
                    { "left": "len", "right": "Returns the number of items in an object" },
                    { "left": "sorted", "right": "Returns a sorted list" },
                    { "left": "type", "right": "Returns the type of an object" }
                ]
            }
        },
        "es": {
            "public_data": {
                "shuffled_left": ["len", "sorted", "type"],
                "shuffled_right": ["Devuelve el número de elementos en un objeto", "Devuelve una lista ordenada", "Devuelve el tipo de un objeto"]
            },
            "private_data": {
                "pairs": [
                    {"left": "len", "right": "Devuelve el número de elementos en un objeto"},
                    {"left": "sorted", "right": "Devuelve una lista ordenada"},
                    {"left": "type", "right": "Devuelve el tipo de un objeto"}
                ]
            }
        }
    }

    
}

async def initialize_test_data(session: AsyncSession):
    """Добавление тестовых данных в базу данных."""
    
    # Проверяем, существует ли квиз
    res = await session.execute(select(Quiz).where(Quiz.id == QUIZ_ID))
    exist_quiz = res.scalars().first()
    
    if not exist_quiz:
        # 1. Создаем квиз
        await session.execute(
            insert(Quiz).values(
                id=QUIZ_ID,
                is_active=True,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
        )

        # 2. Создаем локализации квиза
        quiz_localizations = [
            {
                "id": "b1dfe514-f1cc-4852-a377-cfa7a2007085",
                "quiz_id": QUIZ_ID,
                "language": "EN",
                "title": "Python Programming Quiz",
                "description": "Test your knowledge of Python basics and advanced concepts.",
            },
            {
                "id": "b2dfe514-f1cc-4852-a377-cfa7a2007086",
                "quiz_id": QUIZ_ID,
                "language": "ES",
                "title": "Cuestionario de Programación en Python",
                "description": "Pon a prueba tus conocimientos de conceptos básicos y avanzados de Python.",
            },
            # ... остальные локализации из вашего примера
        ]
        await session.execute(insert(QuizLocalization).values(quiz_localizations))

        # 3. Создаем вопросы
        questions = [
            {
                "id": QUESTION_SINGLE_CHOICE_ID,
                "quiz_id": QUIZ_ID,
                "question_type": "SINGLE_CHOICE",
                "order": 1,
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            },
            {
                "id": QUESTION_MULTIPLE_CHOICE_ID,
                "quiz_id": QUIZ_ID,
                "question_type": "MULTIPLE_CHOICE",
                "order": 2,
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            },
            {
                "id": QUESTION_FILL_BLANK_ID,
                "quiz_id": QUIZ_ID,
                "question_type": "FILL_BLANK",
                "order": 3,
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            },
            {
                "id": QUESTION_MATCHING_ID,
                "quiz_id": QUIZ_ID,
                "question_type": "MATCHING",
                "order": 4,
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            },
        ]
        await session.execute(insert(Question).values(questions))

        # 4. Создаем локализации вопросов
        question_localizations = [
            # SINGLE_CHOICE
            {
                "id": "d1dfe514-f1cc-4852-a377-cfa7a2007091",
                "question_id": QUESTION_SINGLE_CHOICE_ID,
                "language": "EN",
                "question_text": "What is the output of print(2 ** 3)?",
                "content": QUESTION_CONTENTS["single_choice"],
            },
            {
                "id": "d2dfe514-f1cc-4852-a377-cfa7a2007092",
                "question_id": QUESTION_SINGLE_CHOICE_ID,
                "language": "ES",
                "question_text": "¿Cuál es el resultado de print(2 ** 3)?",
                "content": QUESTION_CONTENTS["single_choice"],
            },
            # MULTIPLE_CHOICE
            {
                "id": "e1dfe514-f1cc-4852-a377-cfa7a2007093",
                "question_id": QUESTION_MULTIPLE_CHOICE_ID,
                "language": "EN",
                "question_text": "Which of the following are valid Python data types?",
                "content": QUESTION_CONTENTS["multiple_choice"],
            },
            {
                "id": "e2dfe514-f1cc-4852-a377-cfa7a2007094",
                "question_id": QUESTION_MULTIPLE_CHOICE_ID,
                "language": "ES",
                "question_text": "¿Cuáles de los siguientes son tipos de datos válidos en Python?",
                "content": QUESTION_CONTENTS["multiple_choice"],
            },
            # FILL_BLANK
            {
                "id": "f1dfe514-f1cc-4852-a377-cfa7a2007095",
                "question_id": QUESTION_FILL_BLANK_ID,
                "language": "EN",
                "question_text": "Fill in the blank: The keyword to define a function in Python is ___",
                "content": QUESTION_CONTENTS["fill_blank"],
            },
            {
                "id": "f2dfe514-f1cc-4852-a377-cfa7a2007096",
                "question_id": QUESTION_FILL_BLANK_ID,
                "language": "ES",
                "question_text": "Rellena el espacio en blanco: La palabra clave para definir una función en Python es ___",
                "content": QUESTION_CONTENTS["fill_blank"],
            },
            # MATCHING
            {
                "id": "d1dfe514-f1cc-4852-a377-cfa7a2007092",
                "question_id": QUESTION_MATCHING_ID,
                "language": "EN",
                "question_text": "Match the following Python terms with their descriptions:",
                "content": QUESTION_CONTENTS["matching"]["en"],
            },
            {
                "id": "d2dfe514-f1cc-4852-a377-cfa7a2007093",
                "question_id": QUESTION_MATCHING_ID,
                "language": "ES",
                "question_text": "Relaciona los siguientes términos de Python con sus descripciones:",
                "content": QUESTION_CONTENTS["matching"]["es"],
            },
        ]
        
        await session.execute(insert(QuestionLocalization).values(question_localizations))
        await session.commit() 