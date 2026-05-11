import json

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def to_json(self, **kwargs: any) -> dict:
        data = super().model_dump_json(**kwargs)
        return json.loads(data)
