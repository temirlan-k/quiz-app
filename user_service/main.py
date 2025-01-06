from fastapi import FastAPI
from src.api.v1 import router

def make_app()-> FastAPI:
    app = FastAPI(title='USER SERVICE')
    app.include_router(router)
    return app

app = make_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',port=9002,host='0.0.0.0',reload=True
    )