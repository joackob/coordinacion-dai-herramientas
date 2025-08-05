from dataclasses import dataclass
from src.PaginaDeWord import PaginaDeWord


@dataclass
class Materia:
    nombre: str
    anio_ciclo: str
    campo_formacion: str
    carga_horaria: int
    jefx_de_departamento: str
    docentes: list[str]
    contenido: list[object]
    pass

    def exportar_a_word(self) -> PaginaDeWord:
        return PaginaDeWord()
