from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings

from api import router as api_router
from views import router as views_router
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
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
application.include_router(api_router)
application.include_router(views_router)

application.mount("/static", StaticFiles(directory="app/static"), name="static")


def run():
    uvicorn.run(
        "main:application",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )


if __name__ == "__main__":
    run()
