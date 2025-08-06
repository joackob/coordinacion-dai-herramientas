from typing import Any
from pydantic import BaseModel, model_validator


class BloqueDeContenido(BaseModel):
    id: str
    tipo: str
    contenido: str

    @model_validator(mode="before")
    @classmethod
    def _parsear_bloque_de_informacion(cls, data: Any) -> Any:
        if data["type"] == "paragraph":
            content = data["paragraph"]["text"][0]["plain_text"]
        elif data["type"] == "heading_1":
            content = data["heading_1"]["text"][0]["plain_text"]
        elif data["type"] == "heading_2":
            content = data["heading_2"]["text"][0]["plain_text"]
        elif data["type"] == "heading_3":
            content = data["heading_3"]["text"][0]["plain_text"]
        else:
            content = ""
        return {
            "id": data["id"],
            "tipo": data["type"],
            "contenido": content,
        }
