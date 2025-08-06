import os

import pytest

from src.bases_de_datos_en_notion.materias_en_notion import MateriasEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_tap_entre_las_materias():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos.consultar_por_materia("Taller de Algoritmos y Programación")
    )
    assert (
        taller_de_algoritmos_y_programacion_en_notion.nombre
        == "Taller de Algoritmos y Programación"
    )


@pytest.mark.asyncio
async def test_se_encuentra_los_nombres_materias_de_todas_las_materias_de_dai():
    base_de_datos = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )

    nombres_de_materias = [
        "Taller de Algoritmos y Programación",
        "Algoritmos y Estructuras de Datos",
        "Administración y Gestión de Bases de Datos",
        "Diseño de Software",
        "Diseño Multimedial",
        "Programación Web",
        "Desarrollo de Sistemas",
    ]
    for nombre_de_materia in nombres_de_materias:
        pagina_de_una_materia = await base_de_datos.consultar_por_materia(
            nombre_de_materia
        )
        assert pagina_de_una_materia.nombre == nombre_de_materia
