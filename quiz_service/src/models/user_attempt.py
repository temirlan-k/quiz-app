from datetime import datetime
from typing import List, Optional
import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from src.core.enums import LanguageCode
from src.models import TimestampMixin,Base


class UserAttempt(Base,TimestampMixin):
    __tablename__ = "user_attempts"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        nullable=False
    )
    quiz_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        nullable=False
    )
    question_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )
    session_id: so.Mapped[Optional[uuid.UUID]] = so.mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("user_quiz_sessions.id", ondelete="CASCADE"),
        nullable=True
    )

    answer_content: so.Mapped[dict] = so.mapped_column(
        sa.JSON,
        nullable=False,
        default=dict
    )

    is_correct: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False)

    question: so.Mapped["Question"] = so.relationship(
        back_populates="user_attempts"
    )
    session: so.Mapped[Optional["UserQuizSession"]] = so.relationship(
        back_populates="attempts"
    )

    def __repr__(self) -> str:
        return f"<UserAttempt id={self.id} user={self.user_id} question={self.question_id} is_correct={self.is_correct}>"
