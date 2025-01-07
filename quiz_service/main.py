from fastapi import FastAPI
from src.core.containers import Container
from src.api.v1 import router

def make_app()-> FastAPI:

    container = Container()
    container.wire(packages=["src.api.v1"])

    app = FastAPI(title='QUIZ SERVICE')
    app.container = container
    app.include_router(router)
    return app

app = make_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',port=9000,host='0.0.0.0',reload=True
    )