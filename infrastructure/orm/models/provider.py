from datetime import datetime
from typing import List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.models import Base


class ProviderManagerModel(Base):
    __tablename__ = "provider_manager"
    id: Mapped[str] = mapped_column(primary_key=True, default="code")
    provider_id: Mapped[str] = mapped_column(
        ForeignKey("providers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    telephones: Mapped[str] = mapped_column(nullable=False, unique=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=False)

    provider: Mapped["ProviderModel"] = relationship(back_populates="managers")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ProviderModel(Base):
    __tablename__ = "providers"

    id: Mapped[str] = mapped_column(primary_key=True, default="code")
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=False)
    description: Mapped[str] = mapped_column(nullable=False, unique=False)

    managers: Mapped[List["ProviderManagerModel"]] = relationship(
        back_populates="provider", cascade="all, delete-orphan", lazy="selectin"
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
