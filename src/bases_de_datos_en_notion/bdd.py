import logging

import notion_client as notion


class API:
    _notion_client: notion.AsyncClient

    def __init__(self, notion_api_key: str, log_level=logging.DEBUG):
        self._notion_client = notion.AsyncClient(
            auth=notion_api_key, log_level=log_level
        )


class BDD(API):
    _database_id: str

    def __init__(self, notion_api_key: str, database_id: str, log_level=logging.DEBUG):
        self._database_id = database_id
        super().__init__(notion_api_key, log_level=log_level)
