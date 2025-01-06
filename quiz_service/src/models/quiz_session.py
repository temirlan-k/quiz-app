from datetime import datetime
from typing import List, Optional
import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from src.core.enums import LanguageCode
from src.models import TimestampMixin,Base


class UserQuizSession(Base):
    __tablename__ = "user_quiz_sessions"

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
        sa.ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False
    )

    started_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=sa.func.now(), nullable=False
    )
    ended_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime,
        nullable=True
    )
    is_completed: so.Mapped[bool] = so.mapped_column(
        sa.Boolean,
        default=False
    )


    quiz: so.Mapped["Quiz"] = so.relationship(
        back_populates="sessions"
    )
    attempts: so.Mapped[List["UserAttempt"]] = so.relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return f"<UserQuizSession id={self.id} user={self.user_id} quiz={self.quiz_id}>"
