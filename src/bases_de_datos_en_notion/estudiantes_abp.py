import logging
import random
from src.bases_de_datos_en_notion.bdd import BDD


class Estudiantes(BDD):
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

    async def intentar_cargar_estudiante(self, nombre_completo: str, comision: str):
        try:
            await self._notion_client.pages.create(
                parent={"database_id": self._database_id},
                properties={
                    "Name": {  # Asegúrate de que "Name" coincida con el nombre de la propiedad principal en tu base de datos
                        "title": [{"text": {"content": f"{nombre_completo}"}}]
                    },
                    "Comisión": {"select": {"name": comision}},
                },
                icon={
                    "type": "emoji",
                    "emoji": f"{random.choice(self._iconos)}",
                },
            )
            return self
        except Exception as e:
            logging.error(e)
            raise Exception(f"Error al crear la página para {nombre_completo}")
