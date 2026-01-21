# Склад для автосервисов
import asyncio

from infrastructure.db_helper import db_helper
from infrastructure.orm.positionsMetadataProvider import PositionsMetadataProvider
from services.logger_setup import setup_logging

setup_logging(app_name="storehouse", level="DEBUG")


provider = PositionsMetadataProvider(db=db_helper)
asyncio.run(provider.get_by_id("A-007"))
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
