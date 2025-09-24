from fastapi import FastAPI
from app.api import data_fetch, users
from app.db import base
import logging



app = FastAPI(debug=True)


logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Quantitative Trading Platform Backend")

app.include_router(data_fetch.router, prefix="/data", tags=["data"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up app and creating database tables")
    base.Base.metadata.create_all(bind=base.engine)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Quantitative Trading Platform Backend is running"}
