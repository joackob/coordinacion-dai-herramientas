import os

import pytest

from src.BaseDeDatosEnNotion import BaseDeDatosEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_el_anio_de_tap_entre_las_materias():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos._consultar_por_materia(
            "Taller de Algoritmos y Programación"
        )
    )
    taller_de_algoritmos_y_programacion = (
        taller_de_algoritmos_y_programacion_en_notion.exportar_a_materia()
    )
    assert taller_de_algoritmos_y_programacion.anio == "3ro"


@pytest.mark.asyncio
async def test_se_encuentra_el_anio_de_varias_materias():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
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
        materia_exportada = materia_en_notion.exportar_a_materia()
        assert materia_exportada.anio == materia["anio"]
