import os

import pytest

from src.bases_de_datos_en_notion.materias import Materias


@pytest.mark.asyncio
async def test_cantidad_de_materias_debe_ser_7():
    base_de_datos = Materias(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    materias = await base_de_datos.consultar_por_materias_del_area_dai()

    assert len(materias) == 7


@pytest.mark.asyncio
async def test_cantidad_de_materias_debe_ser_0_al_no_tener_acceso_notion_api():
    with pytest.raises(Exception) as e:
        base_de_datos = Materias(
            notion_api_key="invalid_api_key",
            database_id="invalid_database_id",
        )
        await base_de_datos.consultar_por_materias_del_area_dai()
    assert (
        e.value.args[0]
        == "Error al consultar las materias del área DAI. Verifica tu conexión a Notion."
    )
