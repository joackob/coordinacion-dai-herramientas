from dataclasses import dataclass
import logging
from pprint import pprint

import notion_client as notion

from src.PaginaDeNotion import Materia, MateriaVacia


@dataclass
class MateriasEnNotion:
    _database_id: str
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, database_id: str):
        self._database_id = database_id
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )
        self._nombres_de_materias = [
            "Taller de Algoritmos y Programación",
            "Algoritmos y Estructuras de Datos",
            "Administración y Gestión de Bases de Datos",
            "Diseño de Software",
            "Diseño Multimedial",
            "Programación Web",
            "Desarrollo de Sistemas",
        ]

    async def _consultar_por_materia(self, materia: str) -> Materia:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    "database_id": self._database_id,
                    "filter": {
                        "property": "Nombre",
                        "rich_text": {"contains": materia},
                    },
                }
            )
            return Materia(**respuesta)
        except Exception as e:
            pprint(e)
            return MateriaVacia()

    async def materias(self):
        for nombre_de_materia in self._nombres_de_materias:
            pagina_de_una_materia = await self._consultar_por_materia(nombre_de_materia)
            yield pagina_de_una_materia
