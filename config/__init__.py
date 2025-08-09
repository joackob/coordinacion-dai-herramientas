import pathlib

ubicacion_de_documento_plantilla = pathlib.Path(
    "./templates/programa_template_copia.docx"
)
ubicacion_carpeta_donde_guardar_programas_generados = pathlib.Path("./programas")
if not ubicacion_carpeta_donde_guardar_programas_generados.exists():
    ubicacion_carpeta_donde_guardar_programas_generados.mkdir(parents=True)
