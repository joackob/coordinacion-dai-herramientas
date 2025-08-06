import os

import pytest

from src.bases_de_datos_en_notion.materias_en_notion import MateriasEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_el_anio_de_tap_entre_las_materias():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos._consultar_por_materia(
            "Taller de Algoritmos y Programación"
        )
    )
    assert taller_de_algoritmos_y_programacion_en_notion.anio == "3ro"


@pytest.mark.asyncio
async def test_se_encuentra_el_anio_de_varias_materias():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    materias = [
        {"nombre": "Diseño de Software", "anio": "5to"},
        {"nombre": "Algoritmos y Estructuras de Datos", "anio": "4to"},
        {"nombre": "Taller de Algoritmos y Programación", "anio": "3ro"},
    ]
    for materia in materias:
        materia_en_notion = await base_de_datos._consultar_por_materia(
            materia["nombre"]
        )
        assert materia_en_notion.anio == materia["anio"]
