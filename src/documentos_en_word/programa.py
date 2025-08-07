from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.shared import Pt
from pathlib import Path
from docx.enum.style import WD_STYLE_TYPE

ubicacion_documento_plantilla = "./templates/programa_template copy.docx"


class Programa:
    _docentes: list[str] = []
    _campo_de_formacion: str = "Técnico Especifico - Especialidad TICs"
    _jefe_de_departamento: str = "Andrés Navarro"
    _documento: DocumentObject
    _tabla_con_datos_requeridos: Table

    def __init__(self, asignatura: str, anio_ciclo: str, carga_horaria: int):
        # Abrir el documento de Word que servirá como plantilla
        ubicacion_documento_plantilla_path = Path(ubicacion_documento_plantilla)
        ubicacion_documento_plantilla_path.resolve()
        self._documento = Document(ubicacion_documento_plantilla_path.__str__())

        # Customizar el estilo de los encabezados y parrafos para todo el documento
        documento_con_estilos_por_defecto = Document()
        self._documento.styles.add_style(
            "Heading 2", documento_con_estilos_por_defecto.styles["Heading 2"].type
        )

        self._documento.styles.add_style(
            "Heading 3", documento_con_estilos_por_defecto.styles["Heading 3"].type
        )
        self._documento.styles.add_style(
            "List Bullet", documento_con_estilos_por_defecto.styles["List Bullet"].type
        )
        # self._documento.styles.add_style("Heading 2", WD_STYLE_TYPE.PARAGRAPH)
        # self._documento.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)

        # Obtener la tabla que contiene los datos requeridos
        self._tabla_con_datos_requeridos = self._documento.tables[0]

        # Completar los datos básicos en la tabla del documento
        # Asignatura
        asignatura_en_tabla = self._tabla_con_datos_requeridos.cell(1, 1)
        asignatura_en_tabla.text = asignatura
        # asignatura_en_tabla = asignatura_en_tabla.paragraphs[0]
        # asignatura_en_tabla = asignatura_en_tabla.add_run(asignatura)
        # asignatura_en_tabla.font.size = Pt(14)
        # asignatura_en_tabla.font.bold = True
        # asignatura_en_tabla.font.name = "Arial"
        # Año/Ciclo
        anio_ciclo_en_tabla = self._tabla_con_datos_requeridos.cell(2, 1)
        anio_ciclo_en_tabla.text = anio_ciclo
        # Campo de formación
        campo_de_formacion_en_tabla = self._tabla_con_datos_requeridos.cell(3, 1)
        campo_de_formacion_en_tabla.text = self._campo_de_formacion
        # Carga horaria
        carga_horaria_en_tabla = self._tabla_con_datos_requeridos.cell(4, 1)
        carga_horaria_en_tabla.text = f"{carga_horaria} horas cátedra"
        # Jefe de departamento
        jefe_de_departamento_en_tabla = self._tabla_con_datos_requeridos.cell(5, 1)
        jefe_de_departamento_en_tabla.text = self._jefe_de_departamento
        # Dar estilos requeridos a la celdas que fueron modificadas
        for celda in [
            asignatura_en_tabla,
            anio_ciclo_en_tabla,
            campo_de_formacion_en_tabla,
            carga_horaria_en_tabla,
            jefe_de_departamento_en_tabla,
        ]:
            for parrafo in celda.paragraphs:
                for run in parrafo.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(14)
                    run.font.bold = True

    def agregar_nombres_de_docentes(self, nombres: list[str]):
        self._docentes.extend(nombres)
        docentes_en_tabla = self._tabla_con_datos_requeridos.cell(6, 1)
        docentes_en_tabla = docentes_en_tabla.paragraphs[0].add_run(
            ", ".join(self._docentes)
        )
        docentes_en_tabla.font.name = "Arial"
        docentes_en_tabla.font.size = Pt(14)
        docentes_en_tabla.font.bold = True
        return self

    def separar_tabla_con_datos_del_contenido(self):
        # Insertar un salto de página despues de la primera pagina
        self._documento.add_page_break()

    def guardar(self):
        carpeta_contenedora = Path("./programas")
        ubicacion_final_documento = (
            carpeta_contenedora
            / f"{self._tabla_con_datos_requeridos.cell(1, 1).text.lower().replace(' ', '_')}.docx"
        )
        ubicacion_final_documento.resolve()
        self._documento.save(ubicacion_final_documento.__str__())
        return self
