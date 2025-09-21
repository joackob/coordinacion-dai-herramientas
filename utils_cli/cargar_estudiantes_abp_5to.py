import tqdm
import os
import asyncio
import logging

from src.bases_de_datos_en_notion.estudiantes_abp import Estudiantes

_estudiantes_comision_d = [
    # 5to D
    "Diego Ledezma",
    "Nain Isla",
    "Joaquin Pirilio",
    "Lian Leyenda",
    "Ayelen Quispe",
    "Ariana Villa",
    "Enzo Materazzi",
    "Valentin Velazquez",
    "Rocio Albarracin",
    "Evelyn Villarreal",
    "Abril Herbas",
    "Lucia Acuña",
    "Llusco Mary",
    "Dylan Aragon",
    "Santiago Bunzolino",
    "Juan Manuel Parrado",
    "Fernando Valle",
    "Avila Tomas",
]
_estudiantes_comision_b = [
    # 5to B
    "Sol Perez",
    "Ana Cristina",
    "Julieta Mendoza",
    "Bautista Moyano",
    "Thiago Gomez",
    "Miguel Angel Diaz",
    "Leonardo Ojeda",
    "Karen Diaz",
    "Luana Lopez",
    "Priscila dellatore",
    "Luciano Alcaraz",
    "Gabriel",
    "Luciano Savia",
    "Briseida Uscamayta",
    "Brigit Aguirre",
    "Joel Agustin",
]


async def intentar_cargar_estudiantes_abp_5to():
    try:
        estudiantes = Estudiantes(
            notion_api_key=str(os.getenv("NOTION_API_KEY")),
            database_id=str(os.getenv("ESTUDIANTES_ABP_5_DATABASE_ID")),
            data_source_id=str(os.getenv("ESTUDIANTES_DATA_SOURCE_ID")),
            log_level=logging.ERROR,
        )

        for estudiante in tqdm.tqdm(
            _estudiantes_comision_d,
            desc="Cargando estudiantes 5to D",
        ):
            await estudiantes.cargar_estudiante(estudiante, comision="5to D")

        for estudiante in tqdm.tqdm(
            _estudiantes_comision_b,
            desc="Cargando estudiantes 5to B",
        ):
            await estudiantes.cargar_estudiante(estudiante, comision="5to B")

    except Exception as e:
        logging.error(f"Error: {e}")


def main():
    asyncio.run(intentar_cargar_estudiantes_abp_5to())


if __name__ == "__main__":
    main()
