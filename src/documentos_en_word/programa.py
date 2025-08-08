from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.shared import Pt
from pathlib import Path
from docx.enum.style import WD_STYLE_TYPE
from config import ubicacion_de_documento_plantilla
from config import ubicacion_carpeta_donde_guardar_programas_generados


class Programa:
    _docentes: list[str] = []
    _campo_de_formacion: str = "Técnico Especifico - Especialidad TICs"
    _jefe_de_departamento: str = "Andrés Navarro"
    _documento: DocumentObject
    _tabla_con_datos_requeridos: Table

    def __init__(self, asignatura: str, anio_ciclo: str, carga_horaria: int):
        # Abrir el documento de Word que servirá como plantilla
        ubicacion_de_documento_plantilla.resolve()
        self._documento = Document(f"{ubicacion_de_documento_plantilla}")

        # Agregar estilos que no existen en el documento
        estilo_encabezado_2 = self._documento.styles.add_style(
            "Heading 2", WD_STYLE_TYPE.PARAGRAPH
        )
        estilo_encabezado_2.font.name = "Arial"
        estilo_encabezado_2.font.size = Pt(13)
        estilo_encabezado_2.font.bold = True

        estilo_encabezado_3 = self._documento.styles.add_style(
            "Heading 3", WD_STYLE_TYPE.PARAGRAPH
        )
        estilo_encabezado_3.font.name = "Arial"
        estilo_encabezado_3.font.size = Pt(13)
        estilo_encabezado_3.font.bold = True

        estilo_item_de_lista_desordenada = self._documento.styles.add_style(
            "List Bullet", WD_STYLE_TYPE.PARAGRAPH
        )
        estilo_item_de_lista_desordenada.font.name = "Arial"
        estilo_item_de_lista_desordenada.font.size = Pt(12)
        estilo_item_de_lista_desordenada.paragraph_format.line_spacing = 1.5

        # Obtener la tabla que contiene los datos requeridos
        self._tabla_con_datos_requeridos = self._documento.tables[0]

        # Completar los datos básicos en la tabla del documento
        # Asignatura
        asignatura_en_tabla = self._tabla_con_datos_requeridos.cell(1, 1)
        asignatura_en_tabla.text = asignatura
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
        ubicacion_final_documento = (
            ubicacion_carpeta_donde_guardar_programas_generados
            / f"{self._tabla_con_datos_requeridos.cell(1, 1).text.lower().replace(' ', '_')}.docx"
        )
        ubicacion_final_documento.resolve()
        self._documento.save(ubicacion_final_documento.__str__())
        return self
