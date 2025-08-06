from typing import Any


class Contenido:
    _contenido_plano: str
    pass


class Encabezado2(Contenido):
    pass


class BloqueDeContenido:
    contenido: Contenido

    def __init__(self, data: Any):
        tipo = data["tipo"]
        print(tipo)
        pass
