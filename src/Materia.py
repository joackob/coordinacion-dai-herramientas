from dataclasses import dataclass
from src.PaginaDeWord import PaginaDeWord, PaginaDeWordVacia


@dataclass
class Materia:
    nombre: str
    anio: str
    carga_horaria: int
    jefx_de_departamento: str
    docentes: list[str]
    contenido: list[object]

    def exportar_a_word(self) -> PaginaDeWord:
        return PaginaDeWord()


class MateriaVacia(Materia):
    def __init__(self):
        pass

    def exportar_a_word(self) -> PaginaDeWord:
        return PaginaDeWordVacia()
