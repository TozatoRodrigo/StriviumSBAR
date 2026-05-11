from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType


class HospitalizationActionUserResponse(BaseModel):
    id: UUID = Field(title="User ID")
    first_name: str = Field(title="User Name")
    last_name: str = Field(title="User Last Name")
    member_type: TenantUserMemberType | None = Field(title="User Member Type")
