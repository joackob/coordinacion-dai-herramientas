from src.bases_de_datos_en_notion import BDD
from src.estudiantes.estudiantes import Estudiantes
from src.estudiantes.estudiantes_cud import EstudiantesCUD
from src.materias.materias_en_notion import Materias
from src.materias.materias_en_notion.programas_en_notion import Programas
from src.nomina import Nomina

from src.cli.servicios.configuracion import Configuracion


class Factory:
    def __init__(self, config: Configuracion):
        self._config = config

    def crear_materias(self) -> Materias:
        return Materias(
            notion_api_key=self._config.notion_api_key,
            database_id=self._config.materias_database_id,
            data_source_id=self._config.materias_data_source_id,
            log_level=self._config.log_level,
        )

    def crear_nomina(self) -> Nomina:
        return Nomina(
            notion_api_key=self._config.notion_api_key,
            database_id=self._config.nomina_database_id,
            data_source_id=self._config.nomina_data_source_id,
            log_level=self._config.log_level,
        )

    def crear_programas(self) -> Programas:
        return Programas(
            notion_api_key=self._config.notion_api_key,
            log_level=self._config.log_level,
        )

    def crear_estudiantes(self) -> Estudiantes:
        return Estudiantes(
            notion_api_key=self._config.notion_api_key,
            database_id=self._config.estudiantes_database_id,
            data_source_id=self._config.estudiantes_data_source_id,
            log_level=self._config.log_level,
        )

    def crear_estudiantes_cud(self) -> EstudiantesCUD:
        return EstudiantesCUD(
            notion_api_key=self._config.notion_api_key,
            database_id=self._config.estudiantes_cud_database_id,
            data_source_id=self._config.estudiantes_cud_data_source_id,
            log_level=self._config.log_level,
        )

    def crear_bdd(self, database_id: str, data_source_id: str) -> BDD:
        return BDD(
            notion_api_key=self._config.notion_api_key,
            database_id=database_id,
            data_source_id=data_source_id,
            log_level=self._config.log_level,
        )
