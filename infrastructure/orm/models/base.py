from typing import Mapping, Any

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        mapper = inspect(self).mapper
        return {attr.key: getattr(self, attr.key) for attr in mapper.column_attrs}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], *, ignore_unknown: bool = True):
        cols = {attr.key for attr in inspect(cls).mapper.column_attrs}
        obj = cls()

        for k, v in data.items():
            if k in cols:
                setattr(obj, k, v)
            elif not ignore_unknown:
                raise ValueError(f"Unknown field for {cls.__name__}: {k}")

        return obj
