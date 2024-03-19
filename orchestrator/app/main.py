from fastapi import FastAPI, Request

app = FastAPI()

from .router.utils import router as api_router
from .router.ai import router as ai_router
from .dependencies.database import init_mongo_client, close_mongo_client

app.include_router(api_router, prefix="/utils", tags=["utils"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])

@app.on_event("startup")
async def startup_event():
    init_mongo_client()

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_client()