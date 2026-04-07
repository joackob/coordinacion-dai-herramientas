import os

import pytest

from src.materias.materias_en_notion import Materias
from src.materias.materias_en_notion.programas_en_notion import Programas


@pytest.mark.asyncio
async def test_se_pueden_observar_los_titulos_del_programa_de_tap():
    base_de_datos = Materias(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
        data_source_id=str(os.getenv("MATERIAS_DATA_SOURCE_ID")),
    )
    programas = Programas(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos.intentar_consultar_por_materia_segun_nombre(
            "Taller de Algoritmos y Programación"
        )
    )
    await taller_de_algoritmos_y_programacion_en_notion.descargar_contenido_asociado(
        programas
    )
    # hiper precario
    assert len(taller_de_algoritmos_y_programacion_en_notion._contenido) > 0
