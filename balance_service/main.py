import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from src.core.containers import Container
from src.api.v1 import router
from src.core.consumer import Consumer

@asynccontextmanager
async def lifespan(_:FastAPI):
    cons = Consumer()
    await cons.connect_to_rabbitmq()
    yield


def make_app()-> FastAPI:
    
    container = Container()
    container.wire(packages=["src.api.v1"])
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(router)
    return app

app = make_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',port=9001,host='0.0.0.0',reload=True
    )