import uuid
from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from src.models import Base


class UserQuizSession(Base):
    __tablename__ = "user_quiz_sessions"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True
    )
    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True), nullable=False
    )
    quiz_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    current_streak: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        default=0
    )
    max_streak: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        default=0
    )
    score: so.Mapped[int] = so.mapped_column(
        sa.Integer, default=0, nullable=False
    )
    bonus_questions:so.Mapped[int] = so.mapped_column(
        sa.Integer, default=0, nullable=False
    )
    total_questions: so.Mapped[int] = so.mapped_column(
        sa.Integer, default=0, nullable=False
    )

    started_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=sa.func.now(), nullable=False
    )
    ended_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime, nullable=True
    )

    is_completed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    quiz: so.Mapped["Quiz"] = so.relationship(back_populates="sessions")
    attempts: so.Mapped[List["UserAttempt"]] = so.relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<UserQuizSession id={self.id} user={self.user_id} quiz={self.quiz_id}>"
