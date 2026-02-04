from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from infrastructure.db_helper import db_helper
from api.routes.providers import router as providers_router
from api.routes.providers_managers import router as managers_router
from api.routes.positions import router as positions_router
from api.routes.warehouse import router as warehouses_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.engine.dispose()


app = FastAPI(lifespan=lifespan)


#Роутеры
app.include_router(providers_router)
app.include_router(managers_router)
app.include_router(positions_router)
app.include_router(warehouses_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # файл main.py и переменная app
        host = "127.0.0.1",
        port = 8000,
        reload = True,  # авто-перезагрузка (для разработки)
    )
