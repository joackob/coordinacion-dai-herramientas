import os

import pytest

from src.BaseDeDatosEnNotion import MateriasEnNotion
from src.PaginaDeNotion import MateriaVacia


@pytest.mark.asyncio
async def test_cantidad_de_materias_debe_ser_7():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    materias = []
    async for materia in base_de_datos.materias():
        materias.append(materia)

    assert (
        len([materia for materia in materias if not isinstance(materia, MateriaVacia)])
        == 7
    )


@pytest.mark.asyncio
async def test_cantidad_de_materias_debe_ser_0_al_no_tener_acceso_notion_api():
    base_de_datos = MateriasEnNotion(
        notion_api_key="invalid_api_key",
        database_id="invalid_database_id",
    )
    materias = []
    async for materia in base_de_datos.materias():
        materias.append(materia)

    assert (
        len([materia for materia in materias if not isinstance(materia, MateriaVacia)])
        == 0
    )
