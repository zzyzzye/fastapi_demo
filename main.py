from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.api import api_router
from app.config import settings
from app.core.exceptions import custom_exception_handler
from app.db.session import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时可以在这里清理资源


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
app.add_exception_handler(Exception, custom_exception_handler)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "Welcome to FastAPI Enterprise Demo",
        "docs": f"{settings.API_V1_STR}/docs",
    }
