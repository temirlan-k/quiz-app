import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.v1 import router
from src.core.consumer import Consumer
from src.core.containers import Container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    container: Container = app.container
    consumer: Consumer = container.consumer()
    try:
        await asyncio.sleep(5)
        await consumer.connect_to_rabbit_mq()
        yield
    finally:
        await consumer.close()


def make_app() -> FastAPI:

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
        'main:app', port=9001, host='0.0.0.0', reload=True
    )
