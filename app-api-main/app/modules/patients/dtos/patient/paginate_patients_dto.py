from fastapi import Query
from pydantic import BaseModel


class PaginatePatientsDTO(BaseModel):
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1)
    search: str = Query(None)
