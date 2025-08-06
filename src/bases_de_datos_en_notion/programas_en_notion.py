import logging
from pprint import pprint

import notion_client as notion

from src.paginas_en_notion.bloque import BloqueDeContenido


class ProgramasEnNotion:
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str):
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=logging.DEBUG
        )

    async def consultar_programa_por_materia_id(
        self, materia_id: str
    ) -> list[BloqueDeContenido]:
        try:
            respuesta = await self._notion_client.blocks.children.list(
                block_id=materia_id, page_size=100
            )
            return [BloqueDeContenido(bloque) for bloque in respuesta["results"]]
        except Exception as e:
            pprint(e)
            return []
