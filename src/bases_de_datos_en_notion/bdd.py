import logging

import notion_client as notion


class API:

    def __init__(self, notion_api_key: str, log_level=logging.DEBUG):
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=log_level
        )


class BDD(API):

    def __init__(
        self,
        notion_api_key: str,
        database_id: str,
        data_source_id: str,
        log_level=logging.DEBUG,
    ):
        self._database_id = database_id
        self._data_source_id = data_source_id
        super().__init__(notion_api_key, log_level=log_level)

    def _certificados_para_consultas(self):
        return {
            "database_id": self._database_id,
            "data_sources": [{"id": self._data_source_id}],
        }

    def _certificados_para_crear_paginas(self):
        return {
            "parent": {"type": "data_source_id", "data_source_id": self._data_source_id}
        }
