import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy.exc import IntegrityError

from domain.domain_models.positions import Position
from infrastructure.orm.models import PositionsModel


from infrastructure.db_helper import DatabaseHelper, db_helper


@dataclass
class PositionsMetadataProvider:
    db: DatabaseHelper

    def get_many(self):
        pass

    def get_by_id(self):
        pass

    async def insert_many(self, items: list[Any], refresh: bool = False):
        ok: list[PositionsModel] = []
        failed: list[tuple[Any, str]] = []

        for item in items:
            obj = (
                item
                if isinstance(item, PositionsModel)
                else PositionsModel.from_attrs(item)
            )

            try:
                async with self.db.session(commit=True) as session:
                    session.add(obj)
                    await session.flush()
                    if refresh:
                        await session.refresh(obj)
                ok.append(obj)

            except IntegrityError as e:
                # этот obj не сохранился, но остальные продолжим
                failed.append((item, str(e.orig)))
            except Exception as e:
                failed.append((item, str(e)))
        print(ok, failed)
        return ok, failed

    async def insert(
        self, item: dict[str, Any] | PositionsModel, refresh: bool = True
    ) -> PositionsModel:

        obj = (
            item
            if isinstance(item, PositionsModel)
            else PositionsModel.from_attrs(item)
        )
        async with self.db.session() as session:
            session.add(obj)
            # чтобы obj гарантированно получил PK/дефолты до refresh
            await session.flush()
            if refresh:
                await session.refresh(obj)
            return obj

    def delete_many(self):
        pass

    def delete(self):
        pass

    def update_many(self):
        pass

    def update(self):
        pass


# 1) вставить одну
provider = PositionsMetadataProvider(db=db_helper)
asyncio.run(
    provider.insert_many(
        [
            {
                "id": "A-004",
                "category": "engine",
                "sub_category": "oil",
                "name": "Motor oil 5W-30",
                "description": "Synthetic",
                "balance": 10,
                "min_balance": 2,
                "purchase_price": 20.0,
                "sale_price": 35.0,
                "markup": 1.75,
                "provider": "castrol",
            },
            {
                "id": "A-003",
                "category": "transmission",
                "sub_category": "oil",
                "name": "Motor oil 10W-40",
                "description": "Synthetic",
                "balance": 1011111,
                "min_balance": 2,
                "purchase_price": 2110.0,
                "sale_price": 15.0,
                "markup": 1.5,
                "provider": "lukoil",
            },
            {
                "id": "A-002",
                "category": "transmission",
                "sub_category": "oil",
                "name": "Motor oil 10W-40",
                "description": "Synthetic",
                "balance": 1011111,
                "min_balance": 2,
                "purchase_price": 2110.0,
                "sale_price": 15.0,
            },
        ]
    )
)
