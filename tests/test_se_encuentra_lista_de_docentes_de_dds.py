import os

import pytest

from src.BaseDeDatosEnNotion import BaseDeDatosEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_lista_de_docentes_de_dds():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos._consultar_por_materia("Desarrollo de Sistemas")
    )
    taller_de_algoritmos_y_programacion = (
        taller_de_algoritmos_y_programacion_en_notion.exportar_a_materia()
    )
    assert taller_de_algoritmos_y_programacion.docentes[0] == "Joaquín Blanco"
