import tqdm
import os
import asyncio
import logging

from src.bases_de_datos_en_notion.backlog import Backlog

historias = [
    {
        "titulo": "Historia de Usuario 1",
        "historia": "Como estudiante, quiero poder acceder a los recursos del curso para poder estudiar y completar mis tareas.",
    }
]


async def cargar_historias():
    try:
        backlog = Backlog(
            notion_api_key=str(os.getenv("NOTION_API_KEY")),
            database_id=str(os.getenv("ESTUDIANTES_ABP_5_DATABASE_ID")),
            log_level=logging.ERROR,
        )

        for historia in tqdm.tqdm(
            historias,
            desc="Cargando historias de usuario",
        ):
            await backlog.cargar_nueva_historia(
                titulo=historia["titulo"],
                historia=historia["historia"],
            )
    except Exception as e:
        logging.error(f"Error: {e}")


def main():
    asyncio.run(cargar_historias())


if __name__ == "__main__":
    main()
