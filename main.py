import logging

import click

from src.cli.servicios.configuracion import obtener_log_level
from src.cli.comandos.descargar import descargar
from src.cli.comandos.cargar import cargar
from src.cli.comandos.crear import crear
from src.cli.comandos.cargar_cud import cargar_cud


@click.group()
@click.option(
    "--verbose", "-v", is_flag=True, help="Modo verbose (muestra logs de debug)"
)
@click.pass_context
def cli(ctx, verbose):
    """Coordinación DAI - Herramientas CLI para Notion y documentos"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    log_level = obtener_log_level(verbose)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


@cli.command()
def ayuda():
    """Muestra todos los comandos disponibles"""
    click.echo("""📚 Comandos disponibles:

  descargar programas    Descarga programas de materias por área
  cargar estudiantes      Carga estudiantes ABP 5to en Notion desde archivo
  crear documentos       Crea documentos en Notion desde JSON/CSV
  cargar-cud            Carga estudiantes con CUD desde Excel

  ayuda                 Muestra esta ayuda (este mensaje)
  --help, -h            Muestra la ayuda de un comando específico
""")


@cli.command(name="help-alias")
def help_alias():
    """Alias de 'ayuda' - Muestra todos los comandos disponibles"""
    ayuda()


cli.add_command(descargar)
cli.add_command(cargar)
cli.add_command(crear)
cli.add_command(cargar_cud)


if __name__ == "__main__":
    cli()
