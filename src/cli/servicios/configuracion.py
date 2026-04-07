import logging
import os

import click


def obtener_log_level(verbose: bool) -> int:
    return logging.DEBUG if verbose else logging.ERROR


def obtener_notion_api_key() -> str | None:
    return os.getenv("NOTION_API_KEY")


def validar_notion_api_key() -> None:
    if not obtener_notion_api_key():
        click.echo("Error: NOTION_API_KEY no configurada.", err=True)
        raise click.Abort()


def obtener_database_id(env_var: str) -> str | None:
    return os.getenv(env_var)


def obtener_data_source_id(env_var: str) -> str | None:
    return os.getenv(env_var)


def validar_archivo_existe(ruta: str) -> None:
    if not os.path.exists(ruta):
        click.echo(f"Error: El archivo '{ruta}' no existe.", err=True)
        raise click.Abort()


class Configuracion:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.log_level = obtener_log_level(verbose)

    @property
    def notion_api_key(self) -> str | None:
        return obtener_notion_api_key()

    @property
    def materias_database_id(self) -> str | None:
        return obtener_database_id("MATERIAS_DATABASE_ID")

    @property
    def materias_data_source_id(self) -> str | None:
        return obtener_data_source_id("MATERIAS_DATA_SOURCE_ID")

    @property
    def nomina_database_id(self) -> str | None:
        return obtener_database_id("NOMINA_DATABASE_ID")

    @property
    def nomina_data_source_id(self) -> str | None:
        return obtener_data_source_id("NOMINA_DATA_SOURCE_ID")

    @property
    def estudiantes_database_id(self) -> str | None:
        return obtener_database_id("ESTUDIANTES_DATABASE_ID")

    @property
    def estudiantes_data_source_id(self) -> str | None:
        return obtener_data_source_id("ESTUDIANTES_DATA_SOURCE_ID")

    @property
    def estudiantes_cud_database_id(self) -> str | None:
        return obtener_database_id("ESTUDIANTES_CUD_DATABASE_ID")

    @property
    def estudiantes_cud_data_source_id(self) -> str | None:
        return obtener_data_source_id("ESTUDIANTES_CUD_DATA_SOURCE_ID")

    def validar_estudiantes_cud_config(self) -> None:
        if (
            not self.estudiantes_cud_database_id
            or not self.estudiantes_cud_data_source_id
        ):
            click.echo(
                "Error: Las variables ESTUDIANTES_CUD_DATABASE_ID y "
                "ESTUDIANTES_CUD_DATA_SOURCE_ID no están configuradas.",
                err=True,
            )
            raise click.Abort()
