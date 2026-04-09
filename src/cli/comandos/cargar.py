import asyncio
import json

import click
import pandas as pd
import tqdm

from src.cli.contrato import Command
from src.cli.servicios.configuracion import (
    Configuracion,
    validar_archivo_existe,
    validar_notion_api_key,
)
from src.cli.servicios.factory import Factory


class CargarEstudiantesCommand(Command):
    def __init__(self, archivo: str, config: Configuracion):
        self._archivo = archivo
        self._config = config
        self._factory = Factory(config)

    def execute(self) -> None:
        validar_notion_api_key()
        validar_archivo_existe(self._archivo)
        asyncio.run(self._cargar_estudiantes())

    async def _cargar_estudiantes(self) -> None:
        datos = self._leer_archivo()
        estudiantes = self._factory.crear_estudiantes()

        for fila in tqdm.tqdm(datos, desc="Cargando estudiantes"):
            nombre = fila.get("nombre", "")
            comision = fila.get("comision", "")
            await estudiantes.cargar_estudiante(nombre, comision)

        click.echo(f"✅ Carga de estudiantes completada ({len(datos)} estudiantes).")

    def _leer_archivo(self) -> list[dict]:
        ext = self._archivo.lower().split(".")[-1]

        if ext == "json":
            return self._leer_json()
        elif ext in ("xlsx", "xls"):
            return self._leer_excel()
        else:
            click.echo(
                f"Error: Formato '{ext}' no soportado. Usa JSON o XLSX.", err=True
            )
            raise click.Abort()

    def _leer_json(self) -> list[dict]:
        with open(self._archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                datos = [datos]
            return datos

    def _leer_excel(self) -> list[dict]:
        df = pd.read_excel(self._archivo)
        return df.to_dict(orient="records")


@click.command()
@click.argument("entidad")
@click.option(
    "--archivo",
    required=True,
    help="Ruta al archivo JSON o XLSX con los estudiantes a cargar",
)
@click.pass_context
def cargar(ctx, entidad, archivo):
    """Carga estudiantes ABP 5to en Notion desde archivo

    ENTIDAD: 'estudiantes' (requerido)

    El archivo debe tener las columnas: 'nombre' y 'comision'

    Formatos soportados: JSON, XLSX

    Ejemplos:
      cli cargar estudiantes --archivo datos/estudiantes.json
      cli cargar estudiantes --archivo datos/estudiantes.xlsx
    """
    if entidad != "estudiantes":
        click.echo(
            f"Error: Entidad '{entidad}' no reconocida. Use 'estudiantes'.", err=True
        )
        raise click.Abort()

    verbose = ctx.obj.get("verbose", False)
    config = Configuracion(verbose=verbose)
    command = CargarEstudiantesCommand(archivo=archivo, config=config)
    command.execute()
