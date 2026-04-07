import asyncio
import csv
import json

import click
import tqdm

from src.cli.contrato import Command
from src.cli.servicios.configuracion import (
    Configuracion,
    validar_archivo_existe,
    validar_notion_api_key,
)
from src.cli.servicios.factory import Factory


class CrearDocumentosCommand(Command):
    def __init__(
        self,
        archivo: str,
        database_id: str | None,
        data_source_id: str | None,
        config: Configuracion,
    ):
        self._archivo = archivo
        self._database_id = database_id
        self._data_source_id = data_source_id
        self._config = config
        self._factory = Factory(config)

    def execute(self) -> None:
        validar_notion_api_key()
        validar_archivo_existe(self._archivo)
        self._validar_ids()
        asyncio.run(self._crear_documentos())

    def _validar_ids(self) -> None:
        db_id = self._database_id or self._config.estudiantes_database_id
        ds_id = self._data_source_id or self._config.estudiantes_data_source_id

        if not db_id or not ds_id:
            click.echo(
                "Error: Debes proporcionar --database-id y --data-source-id "
                "o tener las variables de entorno configuradas.",
                err=True,
            )
            raise click.Abort()

        self._database_id = db_id
        self._data_source_id = ds_id

    async def _crear_documentos(self) -> None:
        datos = self._leer_archivo()
        bdd = self._factory.crear_bdd(self._database_id, self._data_source_id)

        exitos = 0
        fallidos = 0
        ext = self._archivo.lower().split(".")[-1]

        for fila in tqdm.tqdm(datos, desc=f"Creando documentos desde {ext}"):
            resultado = await bdd.crear_documento(fila)
            if resultado:
                exitos += 1
            else:
                fallidos += 1

        click.echo(f"✅ Completado: {exitos} exitosos, {fallidos} fallidos.")

    def _leer_archivo(self) -> list[dict]:
        ext = self._archivo.lower().split(".")[-1]

        if ext == "json":
            return self._leer_json()
        elif ext == "csv":
            return self._leer_csv()
        else:
            click.echo(
                f"Error: Formato '{ext}' no soportado. Usa JSON o CSV.", err=True
            )
            raise click.Abort()

    def _leer_json(self) -> list[dict]:
        with open(self._archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                datos = [datos]
            return datos

    def _leer_csv(self) -> list[dict]:
        with open(self._archivo, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)


@click.command()
@click.argument("entidad")
@click.option(
    "--archivo",
    required=True,
    help="Ruta al archivo JSON o CSV con los datos a cargar",
)
@click.option(
    "--database-id",
    help="ID de la base de datos de Notion (también configurable via env var)",
)
@click.option(
    "--data-source-id",
    help="ID del data source de Notion (también configurable via env var)",
)
@click.pass_context
def crear(ctx, entidad, archivo, database_id, data_source_id):
    """Crea documentos en Notion desde un archivo JSON o CSV

    ENTIDAD: Nombre de la entidad (ej: estudiantes, materias, etc.)

    Opciones:
      --archivo         Ruta al archivo JSON o CSV (requerido)
      --database-id     ID de la base de datos de Notion
      --data-source-id  ID del data source de Notion

    El archivo puede ser JSON (array de objetos) o CSV (primera fila = headers).
    Las propiedades se infieren: 'name' o 'title' -> title, demás -> rich_text

    Ejemplos:
      cli crear documentos --archivo datos.json
      cli crear documentos --archivo datos.csv --database-id xxx --data-source-id yyy
    """
    if entidad != "documentos":
        click.echo(
            f"Error: Entidad '{entidad}' no reconocida. Use 'documentos'.", err=True
        )
        raise click.Abort()

    verbose = ctx.obj.get("verbose", False)
    config = Configuracion(verbose=verbose)
    command = CrearDocumentosCommand(
        archivo=archivo,
        database_id=database_id,
        data_source_id=data_source_id,
        config=config,
    )
    command.execute()
