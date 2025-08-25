from fastapi import FastAPI
import uvicorn

from api import router as api_router


app = FastAPI()
app.include_router(
    api_router,
    prefix="/api",
)


if __name__ == "__main__":
    # uvicorn.run("main:app", reload=True)
    uvicorn.run(app)
