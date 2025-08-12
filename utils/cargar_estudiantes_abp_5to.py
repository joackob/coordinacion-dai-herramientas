import os
import asyncio
import logging

from src.bases_de_datos_en_notion.estudiantes_abp import EstudantesABP5toCLI


async def cargar_estudiantes_abp_5to():
    try:
        estudiantes = EstudantesABP5toCLI(
            notion_api_key=str(os.getenv("NOTION_API_KEY")),
            database_id=str(os.getenv("ESTUDIANTES_ABP_5_DATABASE_ID")),
            log_level=logging.ERROR,
        )

        await estudiantes.cargar_y_mostrar_progreso()
    except Exception as e:
        print(f"Error: {e}")


def main():
    asyncio.run(cargar_estudiantes_abp_5to())


if __name__ == "__main__":
    main()
