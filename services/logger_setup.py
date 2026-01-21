from __future__ import annotations

import logging
import logging.config
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    *,
    app_name: str = "storehouse",
    log_dir: str = "logs",
    level: str = "DEBUG",
    console_level: Optional[str] = None,
    file_level: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 10,
) -> None:
    """
    Настраивает логирование для приложения.
    - Пишет в консоль + в файл с ротацией.
    - Уровни можно задать отдельно для консоли/файла.
    """

    # уровни
    level = (level or "INFO").upper()
    console_level = (console_level or level).upper()
    file_level = (file_level or level).upper()

    # папка логов
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logfile = log_path / f"{app_name}.log"

    # единый формат
    fmt = "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": fmt, "datefmt": datefmt},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": console_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": file_level,
                "formatter": "standard",
                "filename": str(logfile),
                "maxBytes": max_bytes,
                "backupCount": backup_count,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": level,
            "handlers": ["console", "file"],
        },
        # Настройка “шумных” логгеров
        "loggers": {
            # SQLAlchemy (если слишком шумно — ставь WARNING)
            "sqlalchemy.engine": {"level": os.getenv("SQLA_LOG_LEVEL", "WARNING")},
            "sqlalchemy.pool": {"level": os.getenv("SQLA_POOL_LOG_LEVEL", "WARNING")},
            # asyncpg обычно молчит, но оставим
            "asyncpg": {"level": os.getenv("ASYNCPG_LOG_LEVEL", "WARNING")},
            # uvicorn (если у тебя FastAPI)
            "uvicorn": {"level": os.getenv("UVICORN_LOG_LEVEL", "INFO")},
            "uvicorn.error": {"level": os.getenv("UVICORN_LOG_LEVEL", "INFO")},
            "uvicorn.access": {
                "level": os.getenv("UVICORN_ACCESS_LOG_LEVEL", "WARNING")
            },
        },
    }

    logging.config.dictConfig(config)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name if name else "storehouse")
