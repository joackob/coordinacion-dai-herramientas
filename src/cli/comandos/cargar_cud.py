import asyncio

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


class CargarEstudiantesCUDCommand(Command):
    def __init__(self, archivo: str, config: Configuracion):
        self._archivo = archivo
        self._config = config
        self._factory = Factory(config)

    def execute(self) -> None:
        validar_notion_api_key()
        validar_archivo_existe(self._archivo)
        self._config.validar_estudiantes_cud_config()
        asyncio.run(self._cargar_estudiantes())

    async def _cargar_estudiantes(self) -> None:
        df = self._leer_excel()
        df = df.dropna(subset=["Estudiante"])

        estudiantes_cud = self._factory.crear_estudiantes_cud()

        exitos = 0
        fallidos = 0

        for _, fila in tqdm.tqdm(
            df.iterrows(), total=len(df), desc="Cargando estudiantes CUD"
        ):
            resultado = await estudiantes_cud.cargar_estudiante(
                nombre=self._obtener_valor(fila, "Estudiante"),
                anio=self._obtener_valor(fila, "Año"),
                division=self._obtener_valor(fila, "Division"),
                diagnostico=self._obtener_valor(fila, "Diagnostico"),
                condicion=self._obtener_valor(fila, "Condición"),
                adecuaciones=self._obtener_valor(fila, "Adecuaciones sugeridas"),
                apnd_acdm=self._obtener_valor(fila, "APND/ACDM"),
                observaciones=self._obtener_valor(fila, "Observaciones"),
                ipp=self._obtener_valor(fila, "IPP"),
            )
            if resultado.cargado:
                exitos += 1
            else:
                fallidos += 1

        click.echo(f"✅ Carga completada: {exitos} exitosos, {fallidos} fallidos.")

    def _leer_excel(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self._archivo)
        except Exception as e:
            click.echo(f"Error al leer el archivo Excel: {e}", err=True)
            raise click.Abort()

    def _obtener_valor(self, fila: pd.Series, columna: str) -> str:
        valor = fila.get(columna, "")
        if pd.notna(valor):
            return str(valor)
        return ""


@click.command()
@click.option(
    "--archivo",
    default="docs/estudiantes-CUD.xlsx",
    help="Ruta al archivo Excel con estudiantes CUD",
)
@click.pass_context
def cargar_cud(ctx, archivo):
    """Carga estudiantes con CUD desde Excel a Notion

    Ejemplos:
      cli cargar-cud
      cli cargar-cud --archivo docs/estudiantes-CUD.xlsx
    """
    verbose = ctx.obj.get("verbose", False)
    config = Configuracion(verbose=verbose)
    command = CargarEstudiantesCUDCommand(archivo=archivo, config=config)
    command.execute()
