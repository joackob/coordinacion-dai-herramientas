import os
import pytest

from src.bases_de_datos_en_notion.materias import MateriasEnNotion
from src.bases_de_datos_en_notion.nomina import Nomina
from src.bases_de_datos_en_notion.programas import Programas
from config import ubicacion_carpeta_donde_guardar_programas_generados


@pytest.mark.asyncio
async def test_crear_archivo_word_con_los_datos_de_tap():
    materias = MateriasEnNotion(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
    )
    nomina = Nomina(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("NOMINA_DATABASE_ID")),
    )
    programas = Programas(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
    )
    nombre_de_la_materia = "Taller de Algoritmos y Programación"
    taller_de_algoritmos_y_programacion_en_notion = (
        await materias.consultar_por_materia_segun_nombre(nombre_de_la_materia)
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

    ubicacion_final_documento = (
        ubicacion_carpeta_donde_guardar_programas_generados
        / f"{nombre_de_la_materia.lower().replace(' ', '_')}.docx"
    )
    ubicacion_final_documento.resolve()
    assert ubicacion_final_documento.exists()
    assert ubicacion_final_documento.is_file()
