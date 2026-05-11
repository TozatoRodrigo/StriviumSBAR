from typing import Annotated

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class CreateTenantRequestDTO(BaseModel):
    name: str
    logo: UploadFile | None = None

    def __init__(
        self,
        name: Annotated[
            str, Form(description="Nome do tenant", examples=["Santa casa"])
        ],
        logo: Annotated[UploadFile | None, File(description="Logo do tenant")] = None,
    ) -> None:
        super().__init__(name=name, logo=logo)
