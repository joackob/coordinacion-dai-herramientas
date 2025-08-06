from typing import Any


class Contenido:
    _contenido_plano: str

    def __init__(self, data: Any):
        if "rich_text" in data and data["rich_text"]:
            self._contenido_plano = "".join(
                fragment.get("text", {}).get("content", "")
                for fragment in data["rich_text"]
            )
        else:
            self._contenido_plano = ""


class Encabezado1(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class Encabezado2(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class Encabezado3(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class Parrafo(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class ListaConViñetas(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class ListaNumerada(Contenido):
    def __init__(self, data: Any):
        super().__init__(data)


class ListaConToDo(Contenido):
    checked: bool

    def __init__(self, data: Any):
        super().__init__(data)
        self.checked = data.get("checked", False)


class Llamada(Contenido):  # callout
    def __init__(self, data: Any):
        super().__init__(data)


class Cite(Contenido):  # quote
    def __init__(self, data: Any):
        super().__init__(data)


class Codigo(Contenido):
    lenguaje: str

    def __init__(self, data: Any):
        super().__init__(data)
        self.lenguaje = data.get("language", "")


class Separador(Contenido):  # divider
    def __init__(self, data: Any):
        self._contenido_plano = "---"  # texto arbitrario, ya que no tiene contenido


class BloqueDeContenido:
    contenido: Contenido

    def __init__(self, data: Any):
        tipo = data["type"]
        bloque = data[tipo]

        if tipo == "paragraph":
            self.contenido = Parrafo(bloque)
        elif tipo == "heading_1":
            self.contenido = Encabezado1(bloque)
        elif tipo == "heading_2":
            self.contenido = Encabezado2(bloque)
        elif tipo == "heading_3":
            self.contenido = Encabezado3(bloque)
        elif tipo == "bulleted_list_item":
            self.contenido = ListaConViñetas(bloque)
        elif tipo == "numbered_list_item":
            self.contenido = ListaNumerada(bloque)
        elif tipo == "to_do":
            self.contenido = ListaConToDo(bloque)
        elif tipo == "callout":
            self.contenido = Llamada(bloque)
        elif tipo == "quote":
            self.contenido = Cite(bloque)
        elif tipo == "code":
            self.contenido = Codigo(bloque)
        elif tipo == "divider":
            self.contenido = Separador(bloque)
        else:
            self.contenido = Contenido(bloque)
