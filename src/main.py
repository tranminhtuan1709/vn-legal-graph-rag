from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interface.routers import retrieval_router

app = FastAPI()

app.include_router(router=retrieval_router, prefix="/retrieve")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
