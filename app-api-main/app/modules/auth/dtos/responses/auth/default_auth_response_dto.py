from pydantic import ConfigDict, Field

from app.concerns.base_model import BaseModel


class DefaultAuthResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(
        description="Token de acesso",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDk5MjcyNDIsInN1YiI6InsnaWQnOiBVVUlEKCcwMzk2YmUyMy0zY2RiLTQ0OTktYjA3Yi1hM2Y3ZWEyYzU2ZGMnKSwgJ2ZpcnN0X25hbWUnOiAnSmhvbicsICdsYXN0X25hbWUnOiAnRG9lJywgJ2VtYWlsJzogJ3l1cmlAZXhhbXBsZS5jb20nfSJ9.mlXO_e6ayyDO08pDpJVydP6y_hdgtMDiXyckXi0-x-0"
        ],
    )
    refresh_token: str = Field(
        description="Token de atualização",
        examples=["TODO"],
    )
    token_type: str = Field(
        description="Tipo de token",
        examples=["Bearer"],
    )
    expires_in: int = Field(
        description="Tempo de expiração do token em minutos",
        examples=[120],
    )
