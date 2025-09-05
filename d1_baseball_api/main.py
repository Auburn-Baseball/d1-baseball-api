from fastapi import FastAPI
from dotenv import load_dotenv
from d1_baseball_api.api.routes import router as api_router
from d1_baseball_api.database import init_supabase

load_dotenv()

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    supabase = init_supabase()
    print(f"Connected to Supabase project")
