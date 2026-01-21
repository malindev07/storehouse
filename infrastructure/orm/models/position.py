from datetime import datetime
from typing import List, Any, Mapping

from sqlalchemy import func, inspect
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
    provider: Mapped[str] = mapped_column(nullable=False, unique=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # def to_dict(self) -> dict:
    #     return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    #
    # @classmethod
    # def from_attrs(cls, src: Any) -> "PositionsModel":
    #     try:
    #         obj = cls()
    #         mapper = inspect(cls)
    #
    #         is_mapping = isinstance(src, Mapping)
    #
    #         # копируем только колонки модели
    #         for col in mapper.columns:
    #             key = col.key
    #
    #             if is_mapping:
    #                 if key in src:
    #                     setattr(obj, key, src[key])
    #             else:
    #                 if hasattr(src, key):
    #                     setattr(obj, key, getattr(src, key))
    #
    #         # проверяем обязательные поля (nullable=False и нет default/server_default)
    #         missing = [
    #             col.key
    #             for col in mapper.columns
    #             if (not col.nullable)
    #             and (col.default is None)
    #             and (col.server_default is None)
    #             and (getattr(obj, col.key, None) is None)
    #         ]
    #         if missing:
    #             raise ValueError(f"Missing required fields: {missing}")
    #
    #         return obj
    #     except Exception as e:
    #         print(str(e), src)


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
