from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings

from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-function
    Зыкрывает сессию после завершения работы приложения
    """
    yield
    await db_helper.dispose()


application = FastAPI(
    lifespan=lifespan,
)
application.include_router(
    api_router,
)


def run():
    uvicorn.run(
        "main:application",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )


if __name__ == "__main__":
    run()
