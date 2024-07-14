from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db, delete_db
from router import router as tasks_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_db()
    print("База очищена")
    await create_db()
    print("База создана")
    yield


@app.on_event("startup")
async def startup_event():
    async with lifespan(app):
        print("Запуск приложения")


@app.on_event("shutdown")
async def shutdown_event():
    print("Остановка приложения")


app.include_router(tasks_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
