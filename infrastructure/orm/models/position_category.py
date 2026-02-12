import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from infrastructure.orm.models import Base


class PositionCategoryModel(Base):
    __tablename__ = "position_category"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )  # лучше уникальное имя
    description: Mapped[str | None] = mapped_column(nullable=True)

    markup: Mapped[float | None] = mapped_column(nullable=True)  # дефолтный коэффициент

    sub_categories: Mapped[list["PositionSubCategoryModel"]] = relationship(
        back_populates="parent_category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


class PositionSubCategoryModel(Base):
    __tablename__ = "position_sub_category"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("position_category.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )  # лучше unique вместе с category_id
    description: Mapped[str | None] = mapped_column(nullable=True)

    markup: Mapped[float | None] = mapped_column(
        nullable=True
    )  # переопределение коэффициента

    parent_category: Mapped["PositionCategoryModel"] = relationship(
        back_populates="sub_categories",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
