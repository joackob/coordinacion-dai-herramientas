import asyncio

import click
import tqdm

from src.cli.contrato import Command
from src.cli.servicios.configuracion import Configuracion, validar_notion_api_key
from src.cli.servicios.factory import Factory


class DescargarProgramasCommand(Command):
    def __init__(self, area: str, config: Configuracion):
        self._area = area
        self._config = config
        self._factory = Factory(config)

    def execute(self) -> None:
        validar_notion_api_key()
        asyncio.run(self._descargar_programas())

    async def _descargar_programas(self) -> None:
        nomina = self._factory.crear_nomina()
        programas = self._factory.crear_programas()

        materias_area = await self._obtener_materias_por_area()
        desc = self._obtener_descripcion()

        for materia in tqdm.tqdm(materias_area, desc=desc):
            await materia.determinar_profesores_a_cargo(nomina)
            await materia.descargar_contenido_asociado(programas)
            documento = materia.crear_documento_para_el_programa()
            documento.guardar()

        click.echo(f"✅ Descarga de programas de {self._area.upper()} completada.")

    async def _obtener_materias_por_area(self):
        materias = self._factory.crear_materias()
        if self._area == "dai":
            return await materias.consultar_por_materias_del_area_dai()
        elif self._area == "pdc":
            return await materias.consultar_por_materias_del_area_pdc()
        elif self._area == "tics":
            return await materias.consultar_por_materias_de_tics()
        elif self._area == "todos":
            dai = await materias.consultar_por_materias_del_area_dai()
            pdc = await materias.consultar_por_materias_del_area_pdc()
            return dai + pdc
        else:
            click.echo(f"Error: Área '{self._area}' no reconocida.", err=True)
            raise click.Abort()

    def _obtener_descripcion(self) -> str:
        return {
            "dai": "Descargando programas de DAI",
            "pdc": "Descargando programas de PDC",
            "tics": "Descargando programas de TICS (DAI + PDC)",
            "todos": "Descargando programas de todas las áreas",
        }.get(self._area, "")


@click.command()
@click.argument("entidad")
@click.option(
    "--area",
    type=click.Choice(["dai", "pdc", "tics", "todos"], case_sensitive=False),
    required=True,
    help="Área/Carrera para descargar programas",
)
@click.pass_context
def descargar(ctx, entidad, area):
    """Descarga programas de materias por área

    ENTIDAD: 'programas' (requerido)

    Áreas disponibles:
      dai   - Diseño de Aplicaciones Informáticas
      pdc   - Procesamiento Digital y Comunicaciones
      tics  - TICS (DAI + PDC)
      todos - Todas las áreas

    Ejemplos:
      cli descargar programas --area dai
      cli descargar programas --area pdc
      cli descargar programas --area tics
      cli descargar programas --area todos
    """
    if entidad != "programas":
        click.echo(
            f"Error: Entidad '{entidad}' no reconocida. Use 'programas'.", err=True
        )
        raise click.Abort()

    verbose = ctx.obj.get("verbose", False)
    config = Configuracion(verbose=verbose)
    command = DescargarProgramasCommand(area=area, config=config)
    command.execute()
