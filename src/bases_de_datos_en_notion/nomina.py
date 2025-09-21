import logging


from src.bases_de_datos_en_notion.bdd import BDD
from src.materias_y_sus_programas.profesor import Profesor


class Nomina(BDD):

    async def consultar_por_profesores_de_una_materia(
        self, materia: str
    ) -> set[Profesor]:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    **self._certificados_para_consultas(),
                    "filter": {
                        "and": [
                            {
                                "property": "Materia",
                                "formula": {"string": {"equals": materia}},
                            },
                            {"property": "Rol", "select": {"equals": "Profesor"}},
                        ]
                    },
                }
            )

            profesores = set([Profesor(dato) for dato in respuesta["results"]])
            return profesores
        except Exception as e:
            logging.error(e)
            return set()
