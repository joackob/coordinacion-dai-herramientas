from dataclasses import dataclass
from src.PaginaDeWord import PaginaDeWord, PaginaDeWordVacia


@dataclass
class Materia:
    nombre: str
    anio_ciclo: str
    campo_formacion: str
    carga_horaria: int
    jefx_de_departamento: str
    docentes: list[str]
    contenido: list[object]

    def esta_vacia(self) -> bool:
        return False

    def exportar_a_word(self) -> PaginaDeWord:
        return PaginaDeWord()


class MateriaVacia(Materia):
    def __init__(self):
        pass

    def exportar_a_word(self) -> PaginaDeWord:
        return PaginaDeWordVacia()

    def esta_vacia(self) -> bool:
        return True
