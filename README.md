# Herramientas para la Coordinación de Áreas Académicas

Este proyecto agrupa diversas herramientas CLI (interfaz de línea de comandos) diseñadas para sistematizar y optimizar operaciones habituales en la coordinación de áreas académicas. El objetivo principal es facilitar la integración, exportación y manejo automatizado de información, especialmente en relación con la plataforma Notion y la gestión de listados de estudiantes.

---

## Funcionalidades principales

- **Integración con Notion:**  
  Conecta y sincroniza información directamente desde la plataforma Notion.

- **Exportación de documentos:**  
  Permite exportar páginas o documentos de Notion a archivos Word de forma rápida y sencilla.

- **Carga automática de listados de estudiantes:**  
  Automatiza la incorporación de listados de alumnos en diversas bases de datos, adaptándose a diferentes áreas y modalidades.

---

## Herramientas disponibles (comandos CLI)

Estas herramientas se ejecutan a través de comandos básicos utilizando `pipenv`:

- `cargar_estudiantes_abp_5to`  
  Carga listados de estudiantes para la modalidad ABP de 5to año.

- `descargar_programas_dai`  
  Descarga y gestiona programas académicos del área DAI.

- `descargar_programas_pdc`  
  Descarga y gestiona programas académicos del área PDC.

- `descargar_programas_tics`  
  Descarga y gestiona programas académicos del área TICs.

---

## Instalación

### Requisitos previos

- **Python 3.12** (recomendado).

  > Si deseas usar otra versión de Python, puedes modificar el requerimiento en el archivo `Pipfile`.

- **pipenv**  
  Instala `pipenv` con el siguiente comando:
  ```bash
  pip install --user pipenv
  ```

### Instalación del proyecto

1. Clona el repositorio o descarga el código fuente.
2. Navega a la carpeta del proyecto en tu terminal.
3. Ejecuta:
   ```bash
   pipenv install -d
   ```
   Esto instalará todas las dependencias y herramientas necesarias para el desarrollo y ejecución.

---

## Uso

Para ejecutar cualquiera de las herramientas, utiliza el comando:

```bash
pipenv run <comando>
```

Por ejemplo:

```bash
pipenv run cargar_estudiantes_abp_5to
pipenv run descargar_programas_dai
```

---

## Notas adicionales

- Si necesitas deshabilitar el requerimiento de Python 3.12, edita el archivo `Pipfile` y ajusta la versión de Python según tus necesidades.
- Consulta la documentación interna de cada comando para más detalles y parámetros adicionales de uso.

---

## Licencia

Este proyecto se distribuye bajo licencia MIT.

---

### Documentación utilizada para este proyecto

- https://developers.notion.com/reference/post-database-query
- https://developers.notion.com/reference/post-page
