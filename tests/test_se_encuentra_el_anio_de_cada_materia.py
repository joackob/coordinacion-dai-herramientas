import os

import pytest

from src.bases_de_datos_en_notion.materias import Materias


@pytest.mark.asyncio
async def test_se_encuentra_el_anio_de_tap_entre_las_materias():
    base_de_datos = Materias(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
        data_source_id=str(os.getenv("MATERIAS_DATA_SOURCE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos.intentar_consultar_por_materia_segun_nombre(
            "Taller de Algoritmos y Programación"
        )
    )
    # hiper precario
    assert taller_de_algoritmos_y_programacion_en_notion._anio == "3ro"
