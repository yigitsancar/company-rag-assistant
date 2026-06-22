from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
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

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
