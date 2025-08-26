import sys
import os

sys.path.append(os.path.dirname(__file__))


from fastapi import FastAPI  # noqa: E402

from api import router as api_router  # noqa: E402
from core.config import settings  # noqa: E402

import uvicorn  # noqa: E402


application = FastAPI()
application.include_router(
    api_router,
    prefix=settings.api.prefix,
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
