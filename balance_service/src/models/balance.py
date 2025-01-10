import uuid
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from src.models import Base


class Balance(Base):

    __tablename__ = "user_balances"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True
    )
    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True), unique=True, nullable=False
    )
    balance: so.Mapped[float] = so.mapped_column(
        sa.DECIMAL(), default=0.0, nullable=False
    )
    last_updated: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, onupdate=sa.func.now(), default=sa.func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Balance(user_id={self.user_id}, balance={self.balance})>"
