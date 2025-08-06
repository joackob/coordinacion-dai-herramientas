from typing import Any


class Profesor:
    _nombre: str
    _apellido: str

    def __init__(self, data: Any):
        propiedades = data["properties"]
        self._nombre = propiedades["Nombre"]["rollup"]["array"][0]["formula"]["string"]
        self._apellido = propiedades["Apellido"]["rollup"]["array"][0]["formula"][
            "string"
        ]

    def __eq__(self, otro_profesor) -> bool:
        if not isinstance(otro_profesor, Profesor):
            return False
        return (
            self._nombre == otro_profesor._nombre
            and self._apellido == otro_profesor._apellido
        )

    def __hash__(self) -> int:
        return hash((self._nombre, self._apellido))

    def __str__(self) -> str:
        return f"{self._nombre} {self._apellido}"
