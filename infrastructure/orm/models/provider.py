import uuid
from datetime import datetime
from typing import List, Mapping, Any

from sqlalchemy import func, ForeignKey, UUID, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.models import Base


class ProviderManagerModel(Base):
    __tablename__ = "provider_manager"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("providers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    telephones: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    provider: Mapped["ProviderModel"] = relationship(
        back_populates="managers", lazy="selectin"
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> dict[str, Any]:
        mapper = inspect(self).mapper
        return {attr.key: getattr(self, attr.key) for attr in mapper.column_attrs}

    @classmethod
    def from_dict_strict(
        cls,
        data: Mapping[str, Any],
        *,
        allow_id: bool = False,
    ) -> "ProviderManagerModel":
        cols = {attr.key for attr in inspect(cls).mapper.column_attrs}

        forbidden = {"created_at", "updated_at"}
        if not allow_id:
            forbidden.add("id")

        extra = set(data.keys()) - cols
        if extra:
            raise ValueError(f"Unknown field(s) for {cls.__name__}: {sorted(extra)}")

        illegal = set(data.keys()) & forbidden
        if illegal:
            raise ValueError(
                f"Forbidden field(s) for {cls.__name__}: {sorted(illegal)}"
            )

        obj = cls()

        for k, v in data.items():
            if k in forbidden:
                continue

            if (
                k in ("id", "provider_id")
                and v is not None
                and not isinstance(v, uuid.UUID)
            ):
                v = uuid.UUID(str(v))

            setattr(obj, k, v)

        required = ("provider_id", "telephones", "name")
        missing = [f for f in required if getattr(obj, f, None) is None]
        if missing:
            raise ValueError(f"Missing required fields for {cls.__name__}: {missing}")

        return obj


class ProviderModel(Base):
    __tablename__ = "providers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # <-- генерим в коде
    )

    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    managers: Mapped[list["ProviderManagerModel"]] = relationship(
        back_populates="provider",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> dict[str, Any]:
        mapper = inspect(self).mapper
        return {attr.key: getattr(self, attr.key) for attr in mapper.column_attrs}

    @classmethod
    def from_dict_strict(
        cls,
        data: Mapping[str, Any],
        *,
        allow_id: bool = False,
    ) -> "ProviderModel":
        cols = {attr.key for attr in inspect(cls).mapper.column_attrs}

        forbidden = {"created_at", "updated_at"}
        if not allow_id:
            forbidden.add("id")

        extra = set(data.keys()) - cols
        if extra:
            raise ValueError(f"Unknown field(s) for {cls.__name__}: {sorted(extra)}")

        illegal = set(data.keys()) & forbidden
        if illegal:
            raise ValueError(
                f"Forbidden field(s) for {cls.__name__}: {sorted(illegal)}"
            )

        obj = cls()

        for k, v in data.items():
            if k in forbidden:
                continue

            if k == "id" and v is not None and not isinstance(v, uuid.UUID):
                v = uuid.UUID(str(v))

            setattr(obj, k, v)

        required = ("name", "address", "description")
        missing = [f for f in required if getattr(obj, f, None) is None]
        if missing:
            raise ValueError(f"Missing required fields for {cls.__name__}: {missing}")

        return obj
