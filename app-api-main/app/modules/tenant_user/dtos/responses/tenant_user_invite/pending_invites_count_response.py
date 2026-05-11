from pydantic import Field

from app.concerns.base_model import BaseModel


class PendingInvitesCountResponse(BaseModel):
    count: int = Field(description="Quantidade de convites pendentes")
