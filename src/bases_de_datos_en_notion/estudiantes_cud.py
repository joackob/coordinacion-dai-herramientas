import logging
import random
from dataclasses import dataclass

from src.bases_de_datos_en_notion.bdd import BDD


@dataclass
class EstudianteCUD:
    nombre: str
    cargado: bool


class EstudiantesCUD(BDD):
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

    async def cargar_estudiante(
        self,
        nombre: str,
        anio: str,
        division: str,
        diagnostico: str,
        condicion: str,
        adecuaciones: str,
        apnd_acdm: str,
        observaciones: str,
        ipp: str,
    ) -> EstudianteCUD:
        try:
            respuesta = await self._notion_client.pages.create(
                **self._certificados_para_crear_paginas(),
                properties={
                    "Estudiante": {"title": [{"text": {"content": nombre}}]},
                    "Año": {"select": {"name": anio}},
                    "División": {"select": {"name": division}},
                },
                icon={
                    "type": "emoji",
                    "emoji": f"{random.choice(EstudiantesCUD._iconos)}",
                },
            )

            page_id = respuesta["id"]
            children = []

            if diagnostico:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "Diagnóstico"}}]
                        },
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": diagnostico}}]
                        },
                    }
                )

            if condicion:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "Condición"}}]
                        },
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"text": {"content": condicion}}]},
                    }
                )

            if adecuaciones:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {"text": {"content": "Adecuaciones sugeridas"}}
                            ]
                        },
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": adecuaciones}}]
                        },
                    }
                )

            if apnd_acdm:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "APND/ACDM"}}]
                        },
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"text": {"content": apnd_acdm}}]},
                    }
                )

            if observaciones:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "Observaciones"}}]
                        },
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": observaciones}}]
                        },
                    }
                )

            if ipp:
                children.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {"rich_text": [{"text": {"content": "IPP"}}]},
                    }
                )
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"text": {"content": ipp}}]},
                    }
                )

            if children:
                await self._notion_client.blocks.children.append(
                    block_id=page_id, children=children
                )

            return EstudianteCUD(nombre=nombre, cargado=True)
        except Exception as e:
            logging.error(e)
            return EstudianteCUD(nombre=nombre, cargado=False)
