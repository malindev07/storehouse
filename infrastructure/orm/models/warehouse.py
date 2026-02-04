import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.models import PositionsModel
from infrastructure.orm.models.base import Base


class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # генерим в коде
    )

    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    # обратная связь
    positions: Mapped[list[PositionsModel]] = relationship(
        back_populates="warehouse",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)
