from dataclasses import dataclass
import logging
from pprint import pprint

import notion_client as notion

from src.paginas_en_notion.materia import Materia, MateriaVacia


@dataclass
class MateriasEnNotion:
    _database_id: str
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, database_id: str):
        self._database_id = database_id
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )
        self._nombres_de_materias_del_area_dai = [
            "Taller de Algoritmos y Programación",
            "Algoritmos y Estructuras de Datos",
            "Administración y Gestión de Bases de Datos",
            "Diseño de Software",
            "Diseño Multimedial",
            "Programación Web",
            "Desarrollo de Sistemas",
        ]

    async def consultar_por_materia(self, materia: str) -> Materia:
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
            return Materia(respuesta)
        except Exception as e:
            pprint(e)
            return MateriaVacia()

    async def consultar_por_programa_de_una_materia_por_su_id(self, materia_id: str):
        try:
            respuesta = await self._notion_client.blocks.children.list(
                block_id=materia_id, page_size=100
            )
            return respuesta
        except Exception as e:
            pprint(e)
            return None

    async def materias_del_area_dai(self):
        for nombre_de_materia in self._nombres_de_materias_del_area_dai:
            pagina_de_una_materia = await self.consultar_por_materia(nombre_de_materia)
            yield pagina_de_una_materia
