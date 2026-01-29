from fastapi import APIRouter
from app.api.login.routes import router as login_router
from app.api.workflows.routes import router as user_workflows_router
from app.api.chat.routes import router as user_chat_router
from app.api.admin.workflows.routes import router as admin_workflows_router
from app.api.admin.users.routes import router as admin_users_router
from app.api.admin.companies.routes import router as admin_companies_router
from app.api.admin.statistics.routes import router as admin_statistics_router

api_router = APIRouter()

# 登录模块
api_router.include_router(login_router, prefix="/auth", tags=["登录"])

# 用户模块
api_router.include_router(user_workflows_router, prefix="/user/workflows", tags=["用户-工作流"])
api_router.include_router(user_chat_router, prefix="/user/chat", tags=["用户-聊天"])

# 管理员模块
api_router.include_router(admin_workflows_router, prefix="/admin/workflows", tags=["管理员-工作流"])
api_router.include_router(admin_users_router, prefix="/admin/users", tags=["管理员-用户"])
api_router.include_router(admin_companies_router, prefix="/admin/companies", tags=["管理员-公司"])
api_router.include_router(admin_statistics_router, prefix="/admin/statistics", tags=["管理员-统计"])