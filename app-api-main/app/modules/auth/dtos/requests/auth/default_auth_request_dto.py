from pydantic import BaseModel, Field


class DefaultAuthRequestDTO(BaseModel):
    login: str = Field(
        description="Login do usuário",
        examples=["jhon.doe@example.com", "123456"],
    )
    password: str = Field(
        description="Senha do usuário",
        examples=["MinhaSenhaForte123@"],
    )
