"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import matters, meta, tools
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="民生办事向导 API —— 不替代政务系统，不直接办理业务",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta.router, prefix=settings.API_PREFIX)
app.include_router(matters.router, prefix=settings.API_PREFIX)
app.include_router(tools.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
