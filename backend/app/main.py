from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator
from app.api.dashboard import router as dashboard_router
from app.api.users import router as users_router
from app.api.health import router as health_router
from app.api.documents import router as documents_router
from app.api.query import router as query_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="Company RAG Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://13.60.237.187:3000",
        "http://13.60.237.187",
        "http://13.62.87.94:3000",
        "http://13.62.87.94",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")

Instrumentator().instrument(app).expose(app)
