import os
import pathlib
import pytest

from src.bases_de_datos_en_notion.materias_en_notion import MateriasEnNotion
from src.bases_de_datos_en_notion.nomina_en_notion import NominaEnNotion
from src.bases_de_datos_en_notion.programas_en_notion import ProgramasEnNotion


@pytest.mark.asyncio
async def test_crear_archivo_word_con_los_datos_de_tap():
    materias = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    nomina = NominaEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("NOMINA_DATABASE_ID")),
    )
    programas = ProgramasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
    )
    nombre_de_la_materia = "Taller de Algoritmos y Programación"
    taller_de_algoritmos_y_programacion_en_notion = (
        await materias.consultar_por_materia(nombre_de_la_materia)
    )

    await taller_de_algoritmos_y_programacion_en_notion.determinar_profesores_a_cargo(
        nomina
    )

    await taller_de_algoritmos_y_programacion_en_notion.descargar_contenido_asociado(
        programas
    )

    taller_de_algoritmos_y_programacion_en_word = (
        taller_de_algoritmos_y_programacion_en_notion
    ).crear_documento_para_el_programa()

    taller_de_algoritmos_y_programacion_en_word.guardar()

    carpeta_contenedora = pathlib.Path("./programas")
    ubicacion_final_documento = (
        carpeta_contenedora / f"{nombre_de_la_materia.lower().replace(' ', '_')}.docx"
    )
    ubicacion_final_documento.resolve()
    assert ubicacion_final_documento.exists()
    assert ubicacion_final_documento.is_file()
