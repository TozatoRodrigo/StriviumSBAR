from fastapi import APIRouter

from .core.environment import envs
from .modules.health.routes import router as health_router

router = APIRouter()

router.include_router(health_router)

if not envs.APP_MODULE or envs.APP_MODULE == "user":
    from .modules.user.routes import router as user_router

    router.include_router(user_router)

if not envs.APP_MODULE or envs.APP_MODULE == "auth":
    from .modules.auth.routes import router as auth_router

    router.include_router(auth_router)

if not envs.APP_MODULE or envs.APP_MODULE == "tenant":
    from .modules.tenant.routes import router as tenant_router

    router.include_router(tenant_router)

if not envs.APP_MODULE or envs.APP_MODULE == "medical-team":
    from .modules.medical_team.routes import router as medical_team_router

    router.include_router(medical_team_router)

if not envs.APP_MODULE or envs.APP_MODULE == "patient":
    from .modules.patients.routes import router as patient_router

    router.include_router(patient_router)


if not envs.APP_MODULE or envs.APP_MODULE == "hospitalization":
    from .modules.hospitalization.routes import router as hospitalization_router

    router.include_router(hospitalization_router)

if not envs.APP_MODULE or envs.APP_MODULE == "hospitalization_action":
    from .modules.hospitalization.routes import hospitalization_action_router

    router.include_router(hospitalization_action_router)

if not envs.APP_MODULE or envs.APP_MODULE == "sbar":
    from .modules.sbar.routes import router as sbar_router

    router.include_router(sbar_router)

if not envs.APP_MODULE or envs.APP_MODULE == "tenant_user":
    from .modules.tenant_user.routers import router as tenant_user_router

    router.include_router(tenant_user_router)

if not envs.APP_MODULE or envs.APP_MODULE == "doctor":
    from .modules.doctor.routes import router as doctor_router

    router.include_router(doctor_router)
