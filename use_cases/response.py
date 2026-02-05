from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class UseCaseResponse:
    success: bool
    msg: str
    params: Dict[str, Any] | None | Any = None
    details: Dict[str, Any] | None | Any = None
