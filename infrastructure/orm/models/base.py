from typing import Mapping, Any

from dotenv import load_dotenv
from sqlalchemy import inspect, MetaData
from sqlalchemy.orm import DeclarativeBase

from infrastructure.orm.settings import Settings

load_dotenv()
schema = Settings().DB_SCHEMA.strip().lower()


class Base(DeclarativeBase):

    metadata = MetaData(schema=schema)

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
