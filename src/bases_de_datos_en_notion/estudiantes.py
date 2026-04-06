import logging
import random

from dataclasses import dataclass

from src.bases_de_datos_en_notion.bdd import BDD


@dataclass
class Estudiante:
    nombre: str
    cargada: bool


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

    async def cargar_estudiante(self, nombre_completo: str, comision: str):
        try:
            await self._notion_client.pages.create(
                # parent={"database_id": self._database_id},
                **self._certificados_para_crear_paginas(),
                properties={
                    "Name": {  # Asegúrate de que "Name" coincida con el nombre de la propiedad principal en tu base de datos
                        "title": [{"text": {"content": f"{nombre_completo}"}}]
                    },
                    "Comisión": {"select": {"name": comision}},
                },
                icon={
                    "type": "emoji",
                    "emoji": f"{random.choice(Estudiantes._iconos)}",
                },
            )
            return Estudiante(nombre=nombre_completo, cargada=True)
        except Exception as e:
            logging.error(e)
            return Estudiante(nombre=nombre_completo, cargada=False)
