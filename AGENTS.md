# AGENTS.md - Guía para Agentes de Código

Este documento proporciona directrices para agentes de código que trabajan en este repositorio.

---

## 1. Comandos de Desarrollo

### Instalación de dependencias

```bash
pipenv install -d
```

### Ejecutar tests

```bash
pipenv run tests
```

Para ejecutar un solo test:

```bash
pipenv run pytest tests/test_nombre_del_test.py::nombre_de_la_funcion
```

Por ejemplo:

```bash
pipenv run pytest tests/test_cantidad_de_materias_del_area_dai.py::test_cantidad_de_materias_debe_ser_7
```

### Formateo de código

```bash
pipenv run format
```

### Linting

```bash
pipenv run pyrefly
```

### Scripts CLI disponibles

```bash
pipenv run cargar_estudiantes_abp_5to
pipenv run cargar_historias
pipenv run descargar_programas_dai
pipenv run descargar_programas_pdc
pipenv run descargar_programas_tics
```

---

## 2. Estructura del Proyecto

```
.
├── src/
│   ├── bases_de_datos_en_notion/  # Integración con Notion API
│   ├── documentos_en_word/         # Generación de documentos Word
│   └── materias_y_sus_programas/   # Modelos de datos de materias
├── tests/                          # Tests unitarios y de integración
├── utils_cli/                      # Scripts CLI
├── templates/                      # Plantillas de documentos
├── config/                         # Configuración global
└── Pipfile                         # Dependencias del proyecto
```

---

## 3. Convenciones de Código

### 3.1 Estilo General

- **Python 3.12+** requerido
- Se usa `black` para formateo automático (línea máxima: 88 caracteres)
- Type hints son obligatorios

### 3.2 Nomenclatura

| Tipo | Convention | Ejemplo |
|------|------------|---------|
| Clases | PascalCase | `Materia`, `BDD` |
| Funciones/métodos | snake_case | `consultar_por_materias_del_area_dai` |
| Variables/atributos | snake_case | `notion_api_key`, `_database_id` |
| Constantes de clase | UPPER_SNAKE_CASE | `_JEFE_DE_DEPARTAMENTO` |
| Atributos privados | underscore prefix | `self._id`, `self._nombre` |

### 3.3 Imports

Orden obligatorio (separados por líneas en blanco):

1. **Biblioteca estándar**: `import os`, `import logging`, `import asyncio`
2. **Paquetes de terceros**: `notion_client`, `pytest`, `docx`
3. **Módulos locales**: `from src.bases_de_datos_en_notion.materias import Materias`

```python
import logging
import os
from typing import Any

import notion_client as notion
import pytest
from docx import Document

from src.bases_de_datos_en_notion.bdd import BDD
from src.materias_y_sus_programas.materia import Materia
```

### 3.4 Type Hints

Usar sintaxis moderna de Python 3.9+: `list[str]`, `set[Profesor]`, etc.

```python
def consultar_materias_por_area(self, area: str) -> list[Materia]:
    ...

def __init__(self, notion_api_key: str, database_id: str, data_source_id: str):
    ...
```

### 3.5 Clases y Herencia

- Usar herencia cuando sea apropiado: `class Materias(BDD)`
- Métodos que retornan `self` permiten method chaining

```python
async def determinar_profesores_a_cargo(self, nomina: Nomina) -> "Materia":
    self._profesores_a_cargo = await nomina.consultar_por_profesores_de_una_materia(
        self._nombre
    )
    return self
```

### 3.6 Async/Await

- Todas las operaciones I/O deben ser async
- Usar `async def` y `await`
- Ejecutar con `asyncio.run()` en el punto de entrada

```python
async def descargar_programas_dai():
    materias = await materias.consultar_por_materias_del_area_dai()

def main():
    asyncio.run(descargar_programas_dai())
```

### 3.7 Manejo de Errores

- Usar bloques `try/except` con logging apropiado
- Loggear errores con `logging.error(e)` antes de re-lanzar

```python
try:
    respuesta = await self._notion_client.databases.query(...)
    return Materia(respuesta["results"][0])
except Exception as e:
    logging.error(e)
    raise Exception(f"Error al consultar la materia '{nombre}'. Verifica tu conexión a Notion.")
```

### 3.8 Docstrings y Comentarios

- NO agregar comentarios a menos que sean necesarios para lógica compleja
- NO escribir docstrings a menos que el usuario lo pida explícitamente

---

## 4. Variables de Entorno

El proyecto requiere un archivo `.env` basado en `.env.example`:

```
NOTION_API_KEY=tu-integracion-secreta
MATERIAS_DATABASE_ID=tu-database-id
NOMINA_DATABASE_ID=tu-database-id
ESTUDIANTES_ABP_5_DATABASE_ID=tu-database-id
BACKLOG_DATABASE_ID=tu-database-id
```

---

## 5. Frameworks y Librerías

| Categoría | Librería |
|-----------|----------|
| Testing | `pytest`, `pytest-asyncio` |
| Formateo | `black` |
| Linting | `pyrefly` |
| Notion API | `notion_client` |
| Documentos Word | `python-docx` |
| CLI | `click`, `tqdm` |
| Validación | `pydantic` |
| Imágenes | `pillow` |

---

## 6. Notas Importantes

1. **No modificar la plantilla**: Los archivos en `templates/` no deben ser modificados
2. **Logs en producción**: Los scripts CLI usan `log_level=logging.ERROR` por defecto
3. **Verificar entorno**: Siempre verificar que las variables de entorno estén configuradas
4. **No crear archivos de documentación**: No crear archivos `.md` a menos que el usuario lo solicite
