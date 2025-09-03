from fastapi import FastAPI
from d1_baseball_api.api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)
