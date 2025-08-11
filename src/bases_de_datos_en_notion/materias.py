from dataclasses import dataclass
import logging
from pprint import pprint

import notion_client as notion

from src.materias_y_sus_programas.materia import Materia


@dataclass
class Materias:
    _database_id: str
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, database_id: str):
        self._database_id = database_id
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )

    async def consultar_por_materia_segun_nombre(self, nombre: str) -> Materia:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    "database_id": self._database_id,
                    "filter": {
                        "property": "Nombre",
                        "rich_text": {"contains": nombre},
                    },
                }
            )
            materia = Materia(respuesta["results"][0])
            return materia
        except Exception as e:
            pprint(e)
            raise Exception(
                f"Error al consultar la materia '{nombre}'. Verifica tu conexión a Notion."
            )

    async def consultar_por_materias_del_area_dai(self) -> list[Materia]:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    "database_id": self._database_id,
                    "filter": {
                        "property": "Área",
                        "select": {"equals": "Diseño de Aplicaciones Informáticas"},
                    },
                }
            )
            materias = [Materia(materia) for materia in respuesta["results"]]
            return materias
        except Exception as e:
            pprint(e)
            raise Exception(
                "Error al consultar las materias del área DAI. Verifica tu conexión a Notion."
            )
