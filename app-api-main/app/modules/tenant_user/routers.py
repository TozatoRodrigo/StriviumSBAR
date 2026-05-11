from fastapi import APIRouter

from app.modules.tenant_user.routes.roles_routes import router as roles_routes
from app.modules.tenant_user.routes.tenant_user_routes import (
    router as tenant_user_routes,
)

router = APIRouter()

router.include_router(roles_routes)
router.include_router(tenant_user_routes)
