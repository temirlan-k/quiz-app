import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declared_attr

Base = so.declarative_base()


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


from src.models.question import Question, QuestionLocalization
from src.models.quiz import Quiz, QuizLocalization
from src.models.quiz_session import UserQuizSession
from src.models.user_attempt import UserAttempt
