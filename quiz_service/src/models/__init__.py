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

async def initialize_test_data(session: AsyncSession):
    """
    Добавление тестовых данных в базу данных.
    """
    # ID квиза
    quiz_id = "a3dfe514-f1cc-4852-a377-cfa7a2007084"

    # Проверяем, существует ли квиз в базе
    res = await session.execute(
        select(Quiz).where(Quiz.id == quiz_id)
    )
    exist_quiz = res.scalars().first()
    print(111,exist_quiz.id)
    if not exist_quiz:
        # Добавляем квиз
        await session.execute(
            insert(Quiz).values(
                id=quiz_id,
                is_active=True,
                created_at="2023-01-01 00:00:00",
                updated_at="2023-01-01 00:00:00",
            )
        )

        # Добавляем локализации для квиза
        await session.execute(
            insert(QuizLocalization).values(
                [
                    {
                        "id": "b1dfe514-f1cc-4852-a377-cfa7a2007085",
                        "quiz_id": quiz_id,
                        "language": "EN",
                        "title": "Python Programming Quiz",
                        "description": "Test your knowledge of Python basics and advanced concepts.",
                    },
                    {
                        "id": "b2dfe514-f1cc-4852-a377-cfa7a2007086",
                        "quiz_id": quiz_id,
                        "language": "ES",
                        "title": "Cuestionario de Programación en Python",
                        "description": "Pon a prueba tus conocimientos de conceptos básicos y avanzados de Python.",
                    },
                    {
                        "id": "b3dfe514-f1cc-4852-a377-cfa7a2007087",
                        "quiz_id": quiz_id,
                        "language": "PT",
                        "title": "Questionário de Programação em Python",
                        "description": "Teste seus conhecimentos sobre os conceitos básicos e avançados de Python.",
                    },
                    {
                        "id": "b4dfe514-f1cc-4852-a377-cfa7a2007088",
                        "quiz_id": quiz_id,
                        "language": "DE",
                        "title": "Python-Programmierung Quiz",
                        "description": "Testen Sie Ihr Wissen über grundlegende und fortgeschrittene Python-Konzepte.",
                    },
                    {
                        "id": "b5dfe514-f1cc-4852-a377-cfa7a2007089",
                        "quiz_id": quiz_id,
                        "language": "TR",
                        "title": "Python Programlama Testi",
                        "description": "Python temel ve ileri düzey kavramlar bilginizi test edin.",
                    },
                    {
                        "id": "b6dfe514-f1cc-4852-a377-cfa7a2007090",
                        "quiz_id": quiz_id,
                        "language": "FR",
                        "title": "Quiz de Programmation Python",
                        "description": "Testez vos connaissances sur les concepts basiques et avancés de Python.",
                    },
                ]
            )
        )

        # Добавляем вопросы
        await session.execute(
            insert(Question).values(
                [
                    {
                        "id": "c1dfe514-f1cc-4852-a377-cfa7a2007084",
                        "quiz_id": quiz_id,
                        "question_type": "SINGLE_CHOICE",
                        "order": 1,
                        "created_at": "2023-01-01 00:00:00",
                        "updated_at": "2023-01-01 00:00:00",
                    },
                    {
                        "id": "c2dfe514-f1cc-4852-a377-cfa7a2007084",
                        "quiz_id": quiz_id,
                        "question_type": "MULTIPLE_CHOICE",
                        "order": 2,
                        "created_at": "2023-01-01 00:00:00",
                        "updated_at": "2023-01-01 00:00:00",
                    },
                    {
                        "id": "c3dfe514-f1cc-4852-a377-cfa7a2007084",
                        "quiz_id": quiz_id,
                        "question_type": "FILL_BLANK",
                        "order": 3,
                        "created_at": "2023-01-01 00:00:00",
                        "updated_at": "2023-01-01 00:00:00",
                    },
                    {
                        "id": "c4dfe514-f1cc-4852-a377-cfa7a2007084",
                        "quiz_id": quiz_id,
                        "question_type": "MATCHING",
                        "order": 4,
                        "created_at": "2023-01-01 00:00:00",
                        "updated_at": "2023-01-01 00:00:00",
                    },
                ]
            )
        )

        # Добавляем локализации для вопросов
        await session.execute(
            insert(QuestionLocalization).values(
                [
                    # SINGLE_CHOICE
                    {
                        "id": "d1dfe514-f1cc-4852-a377-cfa7a2007091",
                        "question_id": "c1dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "EN",
                        "question_text": "What is the output of print(2 ** 3)?",
                        "content": '{"public_data": {"options": [{"id": "opt1", "text": "6"}, {"id": "opt2", "text": "8"}, {"id": "opt3", "text": "9"}]}, "private_data": {"correct_options": ["opt2"]}}',
                    },
                    {
                        "id": "d2dfe514-f1cc-4852-a377-cfa7a2007092",
                        "question_id": "c1dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "ES",
                        "question_text": "¿Cuál es el resultado de print(2 ** 3)?",
                        "content": '{"public_data": {"options": [{"id": "opt1", "text": "6"}, {"id": "opt2", "text": "8"}, {"id": "opt3", "text": "9"}]}, "private_data": {"correct_options": ["opt2"]}}',
                    },
                    # MULTIPLE_CHOICE
                    {
                        "id": "e1dfe514-f1cc-4852-a377-cfa7a2007093",
                        "question_id": "c2dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "EN",
                        "question_text": "Which of the following are valid Python data types?",
                        "content": '{"public_data": {"options": [{"id": "opt1", "text": "int"}, {"id": "opt2", "text": "float"}, {"id": "opt3", "text": "decimal"}]}, "private_data": {"correct_options": ["opt1", "opt2"]}}',
                    },
                    {
                        "id": "e2dfe514-f1cc-4852-a377-cfa7a2007094",
                        "question_id": "c2dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "ES",
                        "question_text": "¿Cuáles de los siguientes son tipos de datos válidos en Python?",
                        "content": '{"public_data": {"options": [{"id": "opt1", "text": "int"}, {"id": "opt2", "text": "float"}, {"id": "opt3", "text": "decimal"}]}, "private_data": {"correct_options": ["opt1", "opt2"]}}',
                    },
                    # FILL_BLANK
                    {
                        "id": "f1dfe514-f1cc-4852-a377-cfa7a2007095",
                        "question_id": "c3dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "EN",
                        "question_text": "Fill in the blank: The keyword to define a function in Python is ___",
                        "content": '{"public_data": {"options": ["def", "function", "lambda"]}, "private_data": {"correct_answers": ["def"]}}',
                    },
                    {
                        "id": "f2dfe514-f1cc-4852-a377-cfa7a2007096",
                        "question_id": "c3dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "ES",
                        "question_text": "Rellena el espacio en blanco: La palabra clave para definir una función en Python es ___",
                        "content": '{"public_data": {"options": ["def", "function", "lambda"]}, "private_data": {"correct_answers": ["def"]}}',
                    },
                    # MATCHING
                    {
                        "id": "d1dfe514-f1cc-4852-a377-cfa7a2007092",
                        "question_id": "c4dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "EN",
                        "question_text": "Match the following Python terms with their descriptions:",
                        "content": '{"public_data": {"pairs": [{"term": "list", "description": "Mutable sequence of elements"}, {"term": "tuple", "description": "Immutable sequence of elements"}, {"term": "dict", "description": "Key-value pairs"}]}, "private_data": {"correct_pairs": {"list": "Mutable sequence of elements", "tuple": "Immutable sequence of elements", "dict": "Key-value pairs"}}}',
                    },
                    {
                        "id": "d2dfe514-f1cc-4852-a377-cfa7a2007093",
                        "question_id": "c4dfe514-f1cc-4852-a377-cfa7a2007084",
                        "language": "ES",
                        "question_text": "Relaciona los siguientes términos de Python con sus descripciones:",
                        "content": '{"public_data": {"pairs": [{"term": "list", "description": "Secuencia mutable de elementos"}, {"term": "tuple", "description": "Secuencia inmutable de elementos"}, {"term": "dict", "description": "Pares clave-valor"}]}, "private_data": {"correct_pairs": {"list": "Secuencia mutable de elementos", "tuple": "Secuencia inmutable de elementos", "dict": "Pares clave-valor"}}}',
                    },
                ]
            )
        )
        await session.commit()
