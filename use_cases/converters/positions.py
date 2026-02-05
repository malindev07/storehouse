from dataclasses import dataclass

from api.schemas.positions.positions import PositionCreateSchema, PositionReadSchema
from domain.positions.positions_domain_model import PositionCreate
from infrastructure.orm.models import PositionsModel


@dataclass
class PositionConverter:

    @staticmethod
    async def create_schema_to_domain(schema: PositionCreateSchema) -> PositionCreate:
        return PositionCreate(
            category=schema.category,
            sub_category=schema.sub_category,
            name=schema.name,
            description=schema.description,
            balance=schema.balance,
            min_balance=schema.min_balance,
            purchase_price=schema.purchase_price,
            markup=schema.markup,
            warehouse_id=schema.warehouse_id,
            provider_id=schema.provider_id,
        )

    async def create_domain_to_model(self, domain: PositionCreate) -> PositionsModel:
        model = PositionsModel(
            category=domain.category,
            sub_category=domain.sub_category,
            name=domain.name,
            description=domain.description,
            balance=domain.balance,
            min_balance=domain.min_balance,
            purchase_price=domain.purchase_price,
            sale_price=domain.sale_price,
            markup=domain.markup,
            # если поставщик может отсутствовать:
            provider_id=domain.provider_id,
            warehouse_id=domain.warehouse_id,
        )
        return model

    async def create_model_to_schema(self, model: PositionsModel) -> PositionReadSchema:
        return PositionReadSchema(
            id=model.id,
            category=model.category,
            sub_category=model.sub_category,
            name=model.name,
            description=model.description,
            balance=model.balance,
            min_balance=model.min_balance,
            purchase_price=model.purchase_price,
            sale_price=model.sale_price,
            markup=model.markup,
            warehouse_id=model.warehouse_id,
            provider_id=model.provider_id,
        )
