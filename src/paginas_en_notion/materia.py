from typing import Any


class Materia:
    _id: str
    _nombre: str
    _anio: str
    _carga_horaria: int

    def __init__(self, data: Any):
        propiedades = data["results"][0]["properties"]
        self._id = data["results"][0]["id"]
        self._nombre = propiedades["Nombre"]["formula"]["string"]
        self._anio = propiedades["Año"]["select"]["name"]
        self._carga_horaria = propiedades["Carga Horaria Semanal"]["number"]

    @property
    def anio(self) -> str:
        return self._anio

    @property
    def nombre(self) -> str:
        return self._nombre


class MateriaVacia(Materia):
    def __init__(self):
        pass

    pass
