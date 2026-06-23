from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.audit.dtos.responses.audit_log_response_dto import AuditLogResponseDTO


class PaginateAuditLogsResponseDTO(BaseModel):
    data: list[AuditLogResponseDTO]
    total: int = Field(title="Número total de registros", examples=[120])
    page: int = Field(title="Número da página atual", examples=[1])
    limit: int = Field(title="Limite por página", examples=[10])
    total_pages: int = Field(title="Número total de páginas", examples=[12])
