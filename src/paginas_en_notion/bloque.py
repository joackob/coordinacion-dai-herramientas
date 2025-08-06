from typing import Any


class Contenido:
    _contenido_plano: str

    def __init__(self, data: Any):
        self._contenido_plano = data["rich_text"][0]["text"]["content"]


class Encabezado2(Contenido):

    def __init__(self, data: Any):
        super().__init__(data)


class Parrafo(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class BloqueDeContenido:
    contenido: Contenido

    def __init__(self, data: Any):
        tipo = data["type"]
        if tipo == "paragraph":
            self.contenido = Parrafo(data[tipo])
        elif tipo == "heading_2":
            self.contenido = Encabezado2(data[tipo])
        else:
            self.contenido = Contenido(data[tipo])
