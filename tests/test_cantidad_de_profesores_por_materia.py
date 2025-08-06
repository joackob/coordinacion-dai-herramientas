import os

import pytest

from src.bases_de_datos_en_notion.nomina_en_notion import NominaEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_lista_de_docentes_de_dds():
    base_de_datos = NominaEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("NOMINA_DATABASE_ID")),
    )
    profesores = await base_de_datos.consultar_por_profesores_al_frente_de_una_materia(
        "Desarrollo de Sistemas"
    )
    assert len(profesores) == 2
