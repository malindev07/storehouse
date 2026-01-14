from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.orm.models.base import Base


class PositionsModel(Base):
    __tablename__ = "positions"

    id: Mapped[str] = mapped_column(primary_key=True, default="code")
    category: Mapped[str] = mapped_column(nullable=False, unique=False)
    sub_category: Mapped[str] = mapped_column(nullable=False, unique=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    description: Mapped[str] = mapped_column(nullable=False, unique=False)
    balance: Mapped[int] = mapped_column(nullable=True)
    min_balance: Mapped[int] = mapped_column(nullable=True)
    purchase_price: Mapped[float] = mapped_column(nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False)
    markup: Mapped[float] = mapped_column(nullable=False)
    provider: Mapped[str] = mapped_column(nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AVGPositionsInfoModel(Base):
    __tablename__ = "avg_positions_info"
    id: Mapped[str] = mapped_column(primary_key=True, default="code")
    category: Mapped[str] = mapped_column(nullable=False, unique=False)
    sub_category: Mapped[str] = mapped_column(nullable=False, unique=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_purchase_price: Mapped[float] = mapped_column(nullable=False)
    last_purchase_price: Mapped[float] = mapped_column(nullable=False)
    avg_purchase_price: Mapped[float] = mapped_column(nullable=False)
    first_sale_price: Mapped[float] = mapped_column(nullable=False)
    last_sale_price: Mapped[float] = mapped_column(nullable=False)
    avg_sale_price: Mapped[float] = mapped_column(nullable=False)
    # providers:Mapped[List] = mapped_column(nullable = False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
