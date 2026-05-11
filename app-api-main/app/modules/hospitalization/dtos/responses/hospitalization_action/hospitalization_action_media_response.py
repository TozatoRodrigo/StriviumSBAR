from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.hospitalization_action_attachment_type_enums import (
    HospitalizationActionAttachmentType,
)


class HospitalizationActionMediaResponse(BaseModel):
    id: UUID = Field(description="ID da mídia")
    type: HospitalizationActionAttachmentType = Field(description="Tipo da mídia")
    file_name: str = Field(description="Nome do arquivo")
    file_path: str = Field(description="Caminho do arquivo")
