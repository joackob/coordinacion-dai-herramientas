from pprint import pprint


from src.bases_de_datos_en_notion.bdd import BDD
from src.materias_y_sus_programas.profesor import Profesor


class Nomina(BDD):

    async def consultar_por_profesores_de_una_materia(
        self, materia: str
    ) -> set[Profesor]:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    "database_id": self._database_id,
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

            return set([Profesor(dato) for dato in respuesta["results"]])

        except Exception as e:
            pprint(e)
            raise Exception(
                f"Error al consultar la nómina de profesores para la materia {materia}: {e}"
            )
