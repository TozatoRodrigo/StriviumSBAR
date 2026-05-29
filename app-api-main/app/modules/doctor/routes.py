from fastapi import APIRouter, Depends, status

from app.enums.models.permissions_enums import DoctorPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.doctor.controllers.doctor_controller import (
    create_doctor,
    delete_doctor,
    get_doctor,
    paginate_doctors,
    update_doctor,
)
from app.modules.doctor.dtos.responses.doctor.detailed_doctor_response import (
    DetailedDoctorResponseDTO,
)
from app.modules.doctor.dtos.responses.doctor.paginate_doctors_response import (
    PaginateDoctorsResponseDTO,
)

router = APIRouter(prefix="/doctor/v1", tags=["doctor"])

router.add_api_route(
    path="/doctors",
    endpoint=create_doctor,
    response_model=DetailedDoctorResponseDTO,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(DoctorPermissionsEnum.CREATE.value)),
    ],
)

router.add_api_route(
    path="/doctors",
    endpoint=paginate_doctors,
    response_model=PaginateDoctorsResponseDTO,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(DoctorPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/doctors/{doctor_id}",
    endpoint=get_doctor,
    response_model=DetailedDoctorResponseDTO,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(DoctorPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/doctors/{doctor_id}",
    endpoint=update_doctor,
    response_model=DetailedDoctorResponseDTO,
    methods=["PUT"],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(DoctorPermissionsEnum.UPDATE.value)),
    ],
)

router.add_api_route(
    path="/doctors/{doctor_id}",
    endpoint=delete_doctor,
    methods=["DELETE"],
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(DoctorPermissionsEnum.DELETE.value)),
    ],
)
