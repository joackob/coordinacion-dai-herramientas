import pathlib

ubicacion_de_documento_plantilla = pathlib.Path(
    "./templates/programa_template_copia.docx"
)
ubicacion_carpeta_donde_guardar_programas_generados = pathlib.Path("./programas")
if not ubicacion_carpeta_donde_guardar_programas_generados.exists():
    ubicacion_carpeta_donde_guardar_programas_generados.mkdir(parents=True)

configuracion_para_logging = {
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "format": '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": "DEBUG",
        },
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
}
