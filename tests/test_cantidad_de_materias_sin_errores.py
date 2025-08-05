from src.BaseDeDatosEnNotion import BaseDeDatosEnNotion

import os
import pytest


@pytest.mark.asyncio
async def test_cantidad_de_materias_debe_ser_8():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
    )
    materias = []
    async for materia in base_de_datos.materias():
        if materia.esta_vacia():
            continue
        materias.append(materia)

    assert len(materias) == 8
