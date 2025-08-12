import os
import logging
import asyncio
import tqdm

from src.bases_de_datos_en_notion.materias import Materias
from src.bases_de_datos_en_notion.nomina import Nomina
from src.bases_de_datos_en_notion.programas import Programas


async def descargar_programas_dai():
    materias = Materias(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("MATERIAS_DATABASE_ID")),
        log_level=logging.ERROR,
    )
    nomina = Nomina(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        database_id=str(os.getenv("NOMINA_DATABASE_ID")),
        log_level=logging.ERROR,
    )
    programas = Programas(
        notion_api_key=str(os.getenv("NOTION_API_KEY")),
        log_level=logging.ERROR,
    )

    materias_de_tics = await materias.consultar_por_materias_de_tics()
    for materia in tqdm.tqdm(materias_de_tics, desc="Descargando programas de DAI"):
        await materia.determinar_profesores_a_cargo(nomina)
        await materia.descargar_contenido_asociado(programas)
        documento = materia.crear_documento_para_el_programa()
        documento.guardar()


def main():
    asyncio.run(descargar_programas_dai())


if __name__ == "__main__":
    main()
