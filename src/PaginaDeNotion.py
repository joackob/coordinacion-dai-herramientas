from src.Materia import Materia


class PaginaDeNotion:
    def __init__(self, datos_primitivos) -> None:
        pass

    def exportar_a_materia(self) -> Materia:
        return Materia(
            nombre="nombre",
            anio_ciclo="2023 - 1",
            campo_formacion="CS",
            carga_horaria=8,
            jefx_de_departamento="jefx de departamento",
            docentes=["docente1", "docente2"],
            contenido=["contenido1", "contenido2"],
        )
