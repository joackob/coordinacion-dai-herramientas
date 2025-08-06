import os

import pytest

from src.BaseDeDatosEnNotion import MateriasEnNotion


@pytest.mark.asyncio
async def test_se_pueden_observar_los_titulos_del_programa_de_tap():
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
