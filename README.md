# FastAPI Enterprise Demo

企业级 FastAPI 项目架构示例

## 项目结构

```
app/
├── api/                      # API 层
│   ├── deps.py              # 依赖注入
│   └── v1/
│       ├── api.py           # 路由聚合
│       └── endpoints/       # 端点
│           ├── auth.py      # 认证
│           └── items.py     # 项目
├── core/                     # 核心模块
│   ├── exceptions.py        # 异常处理
│   └── security.py          # 安全工具
├── db/                       # 数据库
│   └── session.py           # 会话管理
├── models/                   # ORM 模型
│   └── user.py
├── repositories/            # 数据访问层
│   ├── user_repo.py
│   └── item_repo.py
├── schemas/                 # Pydantic 模型
│   └── user.py
├── services/                # 业务逻辑层
│   ├── user_service.py
│   └── item_service.py
├── config.py               # 配置
└── main.py                 # 应用入口
```

## 架构特点

1. **分层架构**：API → Service → Repository → Model
2. **依赖注入**：使用 FastAPI Depends 管理依赖
3. **统一异常**：自定义异常和全局异常处理
4. **安全配置**：JWT Token 认证、密码加密
5. **类型安全**：全程使用 Pydantic 和类型注解

## 使用 uv 运行

```bash
# 安装依赖
uv sync

# 开发运行
uv run uvicorn main:app --reload

# 生产运行
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# 添加新依赖
uv add sqlalchemy

# 添加开发依赖
uv add --dev pytest

# 代码格式化
uv run ruff format .

# 代码检查
uv run ruff check .

# 类型检查
uv run mypy .

# 运行测试
uv run pytest
```

## 访问文档

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API 端点

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户

### 项目
- `POST /api/v1/items/` - 创建项目
- `GET /api/v1/items/` - 获取项目列表
- `GET /api/v1/items/{id}` - 获取项目详情
- `PUT /api/v1/items/{id}` - 更新项目
- `DELETE /api/v1/items/{id}` - 删除项目