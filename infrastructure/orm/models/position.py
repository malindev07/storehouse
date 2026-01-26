import uuid
from datetime import datetime
from typing import List, Any, Mapping

from sqlalchemy import func, inspect, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from infrastructure.orm.models.base import Base


class PositionsModel(Base):
    __tablename__ = "positions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    category: Mapped[str] = mapped_column(nullable=False)
    sub_category: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    balance: Mapped[int | None] = mapped_column(nullable=True)
    min_balance: Mapped[int | None] = mapped_column(nullable=True)

    purchase_price: Mapped[float] = mapped_column(nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False)
    markup: Mapped[float] = mapped_column(nullable=False)

    # если поставщик может отсутствовать:
    provider_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("providers.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    provider: Mapped["ProviderModel | None"] = relationship(lazy="selectin")

    # если хочешь знать конкретного менеджера "кто продал":
    provider_manager_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("provider_manager.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    provider_manager: Mapped["ProviderManagerModel | None"] = relationship(
        lazy="selectin"
    )

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
