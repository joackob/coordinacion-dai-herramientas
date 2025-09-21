import os

import pytest

from src.bases_de_datos_en_notion.nomina import Nomina


@pytest.mark.asyncio
async def test_se_encuentra_lista_de_docentes_de_dds():
    base_de_datos = Nomina(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("NOMINA_DATABASE_ID")),
        data_source_id=str(os.getenv("NOMINA_DATA_SOURCE_ID")),
    )
    profesores = await base_de_datos.consultar_por_profesores_de_una_materia(
        "Desarrollo de Sistemas"
    )
    assert len(profesores) == 1
