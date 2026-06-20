from fastapi import APIRouter, Depends, status

from app.middlewares.auth_middleware import verify_tenant_jwt
from app.modules.patients.controllers.patient_controller import (
    create_patient,
    get_patient,
    paginate_patients,
    update_patient,
)
from app.modules.patients.dtos.responses.patient.paginate_patients_response_dto import (
    PaginatePatientsResponseDTO,
)
from app.modules.patients.dtos.responses.patient.patient_response_dto import (
    PatientResponseDTO,
)

router = APIRouter(
    prefix="/patient/v1",
    tags=["patients"],
)

router.add_api_route(
    path="/patients",
    endpoint=create_patient,
    response_model=PatientResponseDTO,
    methods=["POST"],
    dependencies=[Depends(verify_tenant_jwt)],
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    path="/patients/{patient_id}",
    endpoint=get_patient,
    response_model=PatientResponseDTO,
    methods=["GET"],
    dependencies=[Depends(verify_tenant_jwt)],
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/patients/{patient_id}",
    endpoint=update_patient,
    response_model=PatientResponseDTO,
    methods=["PUT"],
    dependencies=[Depends(verify_tenant_jwt)],
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/patients",
    endpoint=paginate_patients,
    response_model=PaginatePatientsResponseDTO,
    methods=["GET"],
    dependencies=[Depends(verify_tenant_jwt)],
    status_code=status.HTTP_200_OK,
)
