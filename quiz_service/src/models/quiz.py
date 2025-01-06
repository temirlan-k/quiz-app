from typing import Optional
import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from src.core.enums import LanguageCode
from src.models import TimestampMixin,Base



class Quiz(Base,TimestampMixin):
    __tablename__ = 'quizzes'

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True
    )
    title: so.Mapped[str] = so.mapped_column(
        sa.String(50),nullable=False
    )
    description: so.Mapped[str] = so.mapped_column(
        sa.String(50),nullable=True
    )
    is_active: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, default=True
    )
    questions = so.relationship("Question", back_populates="quiz", cascade="all, delete-orphan")


class QuizLocalization(Base):
    __tablename__ = "quiz_localizations"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    quiz_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False
    )
    language: so.Mapped[LanguageCode] = so.mapped_column(
        sa.Enum(LanguageCode),
        nullable=False
    )
    title: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String, nullable=True)

    quiz: so.Mapped["Quiz"] = so.relationship(
        back_populates="localizations"
    )

    __table_args__ = (
        sa.UniqueConstraint("quiz_id", "language", name="uq_quiz_language"),
    )

    def __repr__(self) -> str:
        return f"<QuizLocalization id={self.id} quiz={self.quiz_id} lang={self.language}>"
