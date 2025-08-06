import os

import pytest

from src.bases_de_datos_en_notion.materias_en_notion import MateriasEnNotion


@pytest.mark.skip("Aún no se implementa la descarga del programa de una materia")
@pytest.mark.asyncio
async def test_se_pueden_observar_los_titulos_del_programa_de_tap():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos.consultar_por_materia("Taller de Algoritmos y Programación")
    )
    programa_de_taller_de_algoritmos_y_programacion = (
        await base_de_datos._consultar_por_programa_de_una_materia(
            taller_de_algoritmos_y_programacion_en_notion.id
        )
    )
    assert len(programa_de_taller_de_algoritmos_y_programacion) > 0
