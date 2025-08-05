import os

import pytest

from src.BaseDeDatosEnNotion import BaseDeDatosEnNotion


@pytest.mark.asyncio
async def test_se_encuentra_tap_entre_las_materias():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
    )
    taller_de_algoritmos_y_programacion_en_notion = (
        await base_de_datos._consultar_por_materia(
            "Taller de Algoritmos y Programación"
        )
    )
    taller_de_algoritmos_y_programacion = (
        taller_de_algoritmos_y_programacion_en_notion.exportar_a_materia()
    )
    assert (
        taller_de_algoritmos_y_programacion.nombre
        == "Taller de Algoritmos y Programación"
    )


@pytest.mark.asyncio
async def test_se_encuentra_los_nombres_materias_de_todas_las_materias_de_dai():
    base_de_datos = BaseDeDatosEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("DATABASE_ID")),
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
        pagina_de_una_materia = await base_de_datos._consultar_por_materia(
            nombre_de_materia
        )
        materia = pagina_de_una_materia.exportar_a_materia()
        assert materia.nombre == nombre_de_materia
