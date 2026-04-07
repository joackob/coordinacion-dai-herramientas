import asyncio
import csv
import json
import logging
import os

import click
import pandas as pd
import tqdm

from src.bases_de_datos_en_notion import BDD
from src.estudiantes.estudiantes import Estudiantes
from src.estudiantes.estudiantes_cud import EstudiantesCUD
from src.materias.materias_en_notion import Materias
from src.nomina import Nomina
from src.materias.materias_en_notion.programas_en_notion import Programas


def _obtener_log_level(verbose: bool) -> int:
    return logging.DEBUG if verbose else logging.ERROR


@click.group()
@click.option(
    "--verbose", "-v", is_flag=True, help="Modo verbose (muestra logs de debug)"
)
@click.pass_context
def cli(ctx, verbose):
    """Coordinación DAI - Herramientas CLI para Notion y documentos"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    log_level = _obtener_log_level(verbose)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


@cli.command()
def ayuda():
    """Muestra todos los comandos disponibles"""
    click.echo("""📚 Comandos disponibles:

  descargar programas    Descarga programas de materias por área
  cargar estudiantes      Carga estudiantes ABP 5to en Notion
  cargar estudiantes-cud Carga estudiantes con CUD desde Excel
  crear documentos       Crea documentos en Notion desde JSON/CSV

  ayuda                 Muestra esta ayuda (este mensaje)
  --help, -h            Muestra la ayuda de un comando específico
 """)


@cli.command(name="help-alias")
def help_alias():
    """Alias de 'ayuda' - Muestra todos los comandos disponibles"""
    ayuda()


@cli.command()
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
    log_level = _obtener_log_level(verbose)

    asyncio.run(_descargar_programas(area, log_level))


async def _descargar_programas(area: str, log_level: int):
    notion_key = os.getenv("NOTION_API_KEY")

    materias = Materias(
        notion_api_key=notion_key,
        database_id=os.getenv("MATERIAS_DATABASE_ID"),
        data_source_id=os.getenv("MATERIAS_DATA_SOURCE_ID"),
        log_level=log_level,
    )
    nomina = Nomina(
        notion_api_key=notion_key,
        database_id=os.getenv("NOMINA_DATABASE_ID"),
        data_source_id=os.getenv("NOMINA_DATA_SOURCE_ID"),
        log_level=log_level,
    )
    programas = Programas(
        notion_api_key=notion_key,
        log_level=log_level,
    )

    if area == "dai":
        materias_area = await materias.consultar_por_materias_del_area_dai()
        desc = "Descargando programas de DAI"
    elif area == "pdc":
        materias_area = await materias.consultar_por_materias_del_area_pdc()
        desc = "Descargando programas de PDC"
    elif area == "tics":
        materias_area = await materias.consultar_por_materias_de_tics()
        desc = "Descargando programas de TICS (DAI + PDC)"
    elif area == "todos":
        dai = await materias.consultar_por_materias_del_area_dai()
        pdc = await materias.consultar_por_materias_del_area_pdc()
        materias_area = dai + pdc
        desc = "Descargando programas de todas las áreas"
    else:
        click.echo(f"Error: Área '{area}' no reconocida.", err=True)
        raise click.Abort()

    for materia in tqdm.tqdm(materias_area, desc=desc):
        await materia.determinar_profesores_a_cargo(nomina)
        await materia.descargar_contenido_asociado(programas)
        documento = materia.crear_documento_para_el_programa()
        documento.guardar()

    click.echo(f"✅ Descarga de programas de {area.upper()} completada.")


@cli.command()
@click.argument("entidad")
@click.option(
    "--comision",
    type=click.Choice(["5to-d", "5to-b", "todas"], case_sensitive=False),
    required=True,
    help="Comisión de estudiantes a cargar",
)
@click.pass_context
def cargar(ctx, entidad, comision):
    """Carga estudiantes ABP 5to en Notion

    ENTIDAD: 'estudiantes' (requerido)

    Ejemplos:
      cli cargar estudiantes --comision 5to-d
      cli cargar estudiantes --comision 5to-b
      cli cargar estudiantes --comision todas
    """
    if entidad != "estudiantes":
        click.echo(
            f"Error: Entidad '{entidad}' no reconocida. Use 'estudiantes'.", err=True
        )
        raise click.Abort()

    verbose = ctx.obj.get("verbose", False)
    log_level = _obtener_log_level(verbose)

    asyncio.run(_cargar_estudiantes(comision, log_level))


@cli.command()
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
    log_level = _obtener_log_level(verbose)

    db_id = database_id or os.getenv("ESTUDIANTES_DATABASE_ID")
    ds_id = data_source_id or os.getenv("ESTUDIANTES_DATA_SOURCE_ID")

    if not db_id or not ds_id:
        click.echo(
            "Error: Debes proporcionar --database-id y --data-source-id "
            "o tener las variables de entorno configuradas.",
            err=True,
        )
        raise click.Abort()

    asyncio.run(_crear_desde_archivo(archivo, db_id, ds_id, log_level))


async def _crear_desde_archivo(
    archivo: str, database_id: str, data_source_id: str, log_level: int
):
    notion_key = os.getenv("NOTION_API_KEY")

    if not notion_key:
        click.echo("Error: NOTION_API_KEY no configurada.", err=True)
        raise click.Abort()

    if not os.path.exists(archivo):
        click.echo(f"Error: El archivo '{archivo}' no existe.", err=True)
        raise click.Abort()

    datos = []
    ext = archivo.lower().split(".")[-1]

    try:
        if ext == "json":
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if not isinstance(datos, list):
                    datos = [datos]
        elif ext == "csv":
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                datos = list(reader)
        else:
            click.echo(
                f"Error: Formato '{ext}' no soportado. Usa JSON o CSV.", err=True
            )
            raise click.Abort()
    except Exception as e:
        click.echo(f"Error al leer el archivo: {e}", err=True)
        raise click.Abort()

    if not datos:
        click.echo("El archivo está vacío o no contiene datos.", err=True)
        raise click.Abort()

    bdd = BDD(
        notion_api_key=notion_key,
        database_id=database_id,
        data_source_id=data_source_id,
        log_level=log_level,
    )

    exitos = 0
    fallidos = 0

    for fila in tqdm.tqdm(datos, desc=f"Creando documentos desde {ext}"):
        resultado = await bdd.crear_documento(fila)
        if resultado:
            exitos += 1
        else:
            fallidos += 1

    click.echo(f"✅ Completado: {exitos} exitosos, {fallidos} fallidos.")


async def _cargar_estudiantes(comision: str, log_level: int):
    notion_key = os.getenv("NOTION_API_KEY")

    estudiantes = Estudiantes(
        notion_api_key=notion_key,
        database_id=os.getenv("ESTUDIANTES_DATABASE_ID"),
        data_source_id=os.getenv("ESTUDIANTES_DATA_SOURCE_ID"),
        log_level=log_level,
    )

    if comision == "5to-d":
        for est in tqdm.tqdm(
            _ESTUDIANTES_COMISION_D, desc="Cargando estudiantes 5to D"
        ):
            await estudiantes.cargar_estudiante(est, comision="5to D")
        click.echo("✅ Carga de estudiantes 5to D completada.")
    elif comision == "5to-b":
        for est in tqdm.tqdm(
            _ESTUDIANTES_COMISION_B, desc="Cargando estudiantes 5to B"
        ):
            await estudiantes.cargar_estudiante(est, comision="5to B")
        click.echo("✅ Carga de estudiantes 5to B completada.")
    elif comision == "todas":
        for est in tqdm.tqdm(
            _ESTUDIANTES_COMISION_D, desc="Cargando estudiantes 5to D"
        ):
            await estudiantes.cargar_estudiante(est, comision="5to D")
        for est in tqdm.tqdm(
            _ESTUDIANTES_COMISION_B, desc="Cargando estudiantes 5to B"
        ):
            await estudiantes.cargar_estudiante(est, comision="5to B")
        click.echo("✅ Carga de todas las comisiones completada.")


@cli.command()
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
    log_level = _obtener_log_level(verbose)

    asyncio.run(_cargar_estudiantes_cud(archivo, log_level))


async def _cargar_estudiantes_cud(archivo: str, log_level: int):
    notion_key = os.getenv("NOTION_API_KEY")

    db_id = os.getenv("ESTUDIANTES_CUD_DATABASE_ID")
    ds_id = os.getenv("ESTUDIANTES_CUD_DATA_SOURCE_ID")

    if not db_id or not ds_id:
        click.echo(
            "Error: Las variables ESTUDIANTES_CUD_DATABASE_ID y "
            "ESTUDIANTES_CUD_DATA_SOURCE_ID no están configuradas.",
            err=True,
        )
        raise click.Abort()

    if not os.path.exists(archivo):
        click.echo(f"Error: El archivo '{archivo}' no existe.", err=True)
        raise click.Abort()

    estudiantes_cud = EstudiantesCUD(
        notion_api_key=notion_key,
        database_id=db_id,
        data_source_id=ds_id,
        log_level=log_level,
    )

    try:
        df = pd.read_excel(archivo)
    except Exception as e:
        click.echo(f"Error al leer el archivo Excel: {e}", err=True)
        raise click.Abort()

    df = df.dropna(subset=["Estudiante"])

    exitos = 0
    fallidos = 0

    for _, fila in tqdm.tqdm(
        df.iterrows(), total=len(df), desc="Cargando estudiantes CUD"
    ):
        nombre = str(fila.get("Estudiante", ""))
        anio = str(fila.get("Año", "")) if pd.notna(fila.get("Año")) else ""
        division = (
            str(fila.get("Division", "")) if pd.notna(fila.get("Division")) else ""
        )
        diagnostico = (
            str(fila.get("Diagnostico", ""))
            if pd.notna(fila.get("Diagnostico"))
            else ""
        )
        condicion = (
            str(fila.get("Condición", "")) if pd.notna(fila.get("Condición")) else ""
        )
        adecuaciones = (
            str(fila.get("Adecuaciones sugeridas", ""))
            if pd.notna(fila.get("Adecuaciones sugeridas"))
            else ""
        )
        apnd_acdm = (
            str(fila.get("APND/ACDM", "")) if pd.notna(fila.get("APND/ACDM")) else ""
        )
        observaciones = (
            str(fila.get("Observaciones", ""))
            if pd.notna(fila.get("Observaciones"))
            else ""
        )
        ipp = str(fila.get("IPP", "")) if pd.notna(fila.get("IPP")) else ""

        resultado = await estudiantes_cud.cargar_estudiante(
            nombre=nombre,
            anio=anio,
            division=division,
            diagnostico=diagnostico,
            condicion=condicion,
            adecuaciones=adecuaciones,
            apnd_acdm=apnd_acdm,
            observaciones=observaciones,
            ipp=ipp,
        )
        if resultado.cargado:
            exitos += 1
        else:
            fallidos += 1

    click.echo(f"✅ Carga completada: {exitos} exitosos, {fallidos} fallidos.")


if __name__ == "__main__":
    cli()
