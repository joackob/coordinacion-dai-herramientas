from dataclasses import dataclass
import logging
from pprint import pprint

import notion_client as notion

from src.materias_y_sus_programas.profesor import Profesor


@dataclass
class Nomina:
    _database_id: str
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, database_id: str):
        self._database_id = database_id
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )

    async def consultar_por_profesores_de_una_materia(
        self, materia: str
    ) -> set[Profesor]:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    "database_id": self._database_id,
                    "filter": {
                        "and": [
                            {
                                "property": "Materia",
                                "formula": {"string": {"equals": materia}},
                            },
                            {"property": "Rol", "select": {"equals": "Profesor"}},
                        ]
                    },
                }
            )

            return set([Profesor(dato) for dato in respuesta["results"]])

        except Exception as e:
            pprint(e)
            raise Exception(
                f"Error al consultar la nómina de profesores para la materia {materia}: {e}"
            )
