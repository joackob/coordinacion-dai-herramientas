import random
import logging

from dataclasses import dataclass

from src.bases_de_datos_en_notion.bdd import BDD


@dataclass
class HistoriaDeUsuario:
    titulo: str
    historia: str
    cargada: bool


class Backlog(BDD):
    _iconos = [
        "😊",
        "😃",
        "😄",
        "😁",
        "😎",
        "🥳",
        "🤩",
        "😺",
        "🎈",
        "🌟",
        "🎉",
        "🍀",
        "🦄",
        "🌈",
        "💖",
        "🐣",
        "🍭",
        "🧸",
        "🏅",
        "⚽",
    ]

    async def cargar_nueva_historia(
        self, titulo: str, historia: str
    ) -> HistoriaDeUsuario:
        try:
            await self._notion_client.pages.create(
                parent={"database_id": self._database_id},
                properties={
                    "Name": {"title": [{"text": {"content": f"{titulo}"}}]},
                },
                icon={
                    "type": "emoji",
                    "emoji": f"{random.choice(self._iconos)}",
                },
                children=[
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "Historia de Usuario"}}]
                        },
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"text": {"content": historia}}]},
                    },
                ],
            )
            return HistoriaDeUsuario(titulo=titulo, historia=historia, cargada=True)
        except Exception as e:
            logging.error(f"Error al cargar la historia: {e}")
            return HistoriaDeUsuario(titulo=titulo, historia=historia, cargada=False)
