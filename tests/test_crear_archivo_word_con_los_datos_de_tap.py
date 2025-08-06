import os

import pytest

from src.bases_de_datos_en_notion.materias_en_notion import MateriasEnNotion


@pytest.mark.asyncio
async def test_crear_archivo_word_con_los_datos_de_tap():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos.consultar_por_materia("Taller de Algoritmos y Programación")
    )

    taller_de_algoritmos_y_programacion_en_word = (
        await taller_de_algoritmos_y_programacion_en_notion.crear_documento_para_el_programa()
    )

    taller_de_algoritmos_y_programacion_en_word.guardar()

    # hiper precario
    assert taller_de_algoritmos_y_programacion_en_notion._anio == "3ro"
