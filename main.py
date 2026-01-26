# Склад для автосервисов
import asyncio

from infrastructure.db_helper import db_helper
from infrastructure.orm.metadata_providers.positionsMetadataProvider import (
    PositionsMetadataProvider,
)
from infrastructure.orm.metadata_providers.providerManagerMetadataProvider import (
    ProviderManagerMetadataProvider,
)
from infrastructure.orm.metadata_providers.providersMetadataProvider import (
    ProviderMetadataProvider,
)
from infrastructure.orm.models import ProviderManagerModel
from services.logger_setup import setup_logging

setup_logging(app_name="storehouse", level="DEBUG")


position_metadata = PositionsMetadataProvider(db=db_helper)
provider_metadata = ProviderMetadataProvider(db=db_helper)
manager_provider = ProviderManagerMetadataProvider(db=db_helper)
manager_data = {
    "provider_id": "6f1a7e9a-4f55-4a7c-9b4b-25d6c5d0f1c2",
    "name": "Иван Петров",
    "telephones": "+7 (999) 123-45-67",
}
manager_data["provider_id"] = (
    "d71bb060-c59c-4f0e-9c55-cd6692f55846"  # можно UUID, можно строкой (у тебя конвертируется)
)
manager = ProviderManagerModel.from_dict_strict(manager_data, allow_id=False)

provider_data = {
    "name": "ООО «ГазСервис Север»",
    "address": "г. Москва, ул. Примерная, 10",
    "description": "Поставщик комплектующих и расходников для ГБО. Работаем по договору, безнал/нал.",
}
asyncio.run(manager_provider.insert(data=manager_data))
# asyncio.run(
#     provider.update_by_id(position_id="A-003", data={"sub_category": "oilllll"})
# )
# asyncio.run(
#     provider.insert_many(
#         [
#             {
#                 "id": "A-007",
#                 "category": "engine",
#                 "sub_category": "oil",
#                 "name": "Motor oil 5W-30",
#                 "description": "Synthetic",
#                 "balance": 10,
#                 "min_balance": 2,
#                 "purchase_price": 20.0,
#                 "sale_price": 35.0,
#                 "markup": 1.75,
#                 "provider": "castrol",
#             },
#             {
#                 "id": "A-008",
#                 "category": "transmission",
#                 "sub_category": "oil",
#                 "name": "Motor oil 10W-40",
#                 "description": "Synthetic",
#                 "balance": 1011111,
#                 "min_balance": 2,
#                 "purchase_price": 2110.0,
#                 "sale_price": 15.0,
#                 "markup": 1.5,
#                 "provider": "lukoil",
#             },
#             {
#                 "id": "A-002",
#                 "category": "transmission",
#                 "sub_category": "oil",
#                 "name": "Motor oil 10W-40",
#                 "description": "Synthetic",
#                 "balance": 1011111,
#                 "min_balance": 2,
#                 "purchase_price": 2110.0,
#                 "sale_price": 15.0,
#             },
#         ]
#     )
# )
