import enum
from typing import List
import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from src.core.enums import LanguageCode, QuestionType
from src.models import TimestampMixin, Base


class Question(Base, TimestampMixin):
    __tablename__ = 'questions'

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True
    )
    quiz_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.ForeignKey('quizzes.id', ondelete='CASCADE'),
        nullable=False
    )
    question_type: so.Mapped[QuestionType] = so.mapped_column(
        sa.Enum(QuestionType), nullable=False
    )
    content: so.Mapped[dict] = so.mapped_column(sa.JSON, nullable=False, default=dict)
    order: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, default=1)

    quiz = so.relationship("Quiz", back_populates="questions")
    localizations: so.Mapped[List["QuestionLocalization"]] = so.relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )
    user_attempts: so.Mapped[List["UserAttempt"]] = so.relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Question id={self.id} type={self.question_type}>"


class QuestionLocalization(Base):
    __tablename__ = "question_localizations"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True
    )
    question_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )
    language: so.Mapped[LanguageCode] = so.mapped_column(
        sa.Enum(LanguageCode),
        nullable=False
    )
    question_text: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    content: so.Mapped[dict] = so.mapped_column(
        sa.JSON,
        nullable=False,
        default=dict
    )

    question = so.relationship("Question", back_populates="localizations")

    __table_args__ = (
        sa.UniqueConstraint('question_id', 'language', name='uq_question_language'),
    )

    def __repr__(self) -> str:
        return f"<QuestionLocalization id={self.id} question={self.question_id} lang={self.language}>"
