from typing import Annotated
from pydantic import BaseModel, Secret
from pydantic.types import StringConstraints
import logging
from pprint import pprint

import notion_client as notion

from src.PaginaDeNotion import PaginaDeNotion

# tal vez lo use para alguna clase de credenciales, no lo borro
ClaveNoVacia = Secret[Annotated[str, StringConstraints(min_length=8)]]


class BaseDeDatosEnNotion(BaseModel):
    _notion_api_key: str
    _database_id: str
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, database_id: str):
        self._notion_api_key = notion_api_key
        self._database_id = database_id
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )
        self._nombres_de_materias = [
            "Taller de Algoritmos y Programación",
            "Taller de Tecnologías de la Representación",
            "Algoritmos y Estructuras de Datos",
            "Administración y Gestión de Base de Datos",
            "Diseño de Software",
            "Diseño Multimedial",
            "Programación Web",
            "Desarrollo de Sistemas",
        ]

    async def _consultar_por_materia(self, materia: str):
        try:
            return await self._notion_client.databases.query(
                **{
                    "database_id": str(self._database_id),
                    "filter": {
                        "property": "Nombre",
                        "rich_text": {"contains": materia},
                    },
                }
            )
        except Exception as e:
            pprint(e)
            raise Exception(
                f"Error al consultar la base de datos de Notion: {e}"
            ) from e

    async def materias(self):
        for nombre_de_materia in self._nombres_de_materias:
            respuesta = await self._consultar_por_materia(nombre_de_materia)
            pagina_de_una_materia = PaginaDeNotion(respuesta)
            yield pagina_de_una_materia.exportar_a_materia()
