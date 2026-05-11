from pydantic import BaseModel, Field


class ExceptionDTO(BaseModel):
    message: str = Field(description="Mensagem de erro")
