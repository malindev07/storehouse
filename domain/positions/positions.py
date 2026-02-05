from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Mapping

from dotenv.parser import Position

from domain.positions.positions_domain_model import PositionCreate
from services.logger_setup import setup_logging, get_logger

setup_logging(level="DEBUG")
log = get_logger(__name__)


@dataclass(slots=True, frozen=True)
class PositionDomain:

    money_scale: str = "0.01"  # округление цены до копеек

    async def create(self, position: PositionCreate) -> PositionCreate:
        # TODO сделать правильный расчет в процентах
        if position.sale_price is None:
            position.sale_price = round(position.purchase_price * position.markup, 2)

        return position
