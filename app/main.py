from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api import router as api_router
from core.config import settings
from core.models import db_helper
from views import router as views_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-function
    Зыкрывает сессию после завершения работы приложения
    """
    yield
    await db_helper.dispose()


application = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
application.include_router(api_router)
application.include_router(views_router)

os.makedirs("static/uploads/recipes", exist_ok=True)
application.mount(
    "/static/uploads",
    StaticFiles(directory="/app/static/uploads"),
    name="uploads",
)
application.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
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
