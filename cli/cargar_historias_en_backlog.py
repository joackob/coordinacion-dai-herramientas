import tqdm
import os
import asyncio
import logging

from src.bases_de_datos_en_notion.backlog import Backlog

historias = [
    {
        "titulo": "Identificación automática del usuario",
        "historia": "Como usuario, quiero que la báscula me reconozca automáticamente al subirme, para que mis mediciones se registren en mi perfil sin necesidad de ingresar datos manualmente.",
    },
    {
        "titulo": "Registro histórico de mediciones",
        "historia": "Como usuario, quiero que la báscula guarde un historial de mis pesos y otras métricas, para poder monitorear mi progreso a lo largo del tiempo desde la aplicación.",
    },
    {
        "titulo": "Sincronización con aplicaciones móviles",
        "historia": "Como usuario, quiero que los datos de la báscula se sincronicen automáticamente con mi celular, para consultar mis registros y recibir recomendaciones personalizadas.",
    },
    {
        "titulo": "Alertas y recomendaciones personalizadas",
        "historia": "Como usuario, quiero recibir alertas y recomendaciones basadas en mis mediciones y tendencias, para mejorar mis hábitos y alcanzar mis objetivos de salud.",
    },
    {
        "titulo": "Soporte para múltiples perfiles",
        "historia": "Como familia, quiero que la báscula pueda reconocer y gestionar varios perfiles de usuario, para que cada integrante tenga su propio registro y recomendaciones personalizadas.",
    },
    {
        "titulo": "Privacidad y seguridad de los datos",
        "historia": "Como usuario, quiero que mis datos personales y de salud estén protegidos y solo sean accesibles por mí, para asegurar la privacidad y confidencialidad de mi información.",
    },
]


async def cargar_historias():
    try:
        backlog = Backlog(
            notion_api_key=str(os.getenv("NOTION_API_KEY")),
            database_id=str(os.getenv("BACKLOG_DATABASE_ID")),
            data_source_id=str(os.getenv("BACKLOG_DATA_SOURCE_ID")),
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
