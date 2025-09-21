import logging


from src.materias_y_sus_programas.materia import Materia
from src.bases_de_datos_en_notion.bdd import BDD


class Materias(BDD):

    async def intentar_consultar_por_materia_segun_nombre(self, nombre: str) -> Materia:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    **self._certificados_para_consultas(),
                    "filter": {
                        "property": "Nombre",
                        "rich_text": {"contains": nombre},
                    },
                }
            )
            materia = Materia(respuesta["results"][0])
            return materia
        except Exception as e:
            logging.error(e)
            raise Exception(
                f"Error al consultar la materia '{nombre}'. Verifica tu conexión a Notion."
            )

    async def consultar_materias_por_area(self, area: str) -> list[Materia]:
        try:
            respuesta = await self._notion_client.databases.query(
                **{
                    # "database_id": self._database_id,
                    **self._certificados_para_consultas(),
                    "filter": {
                        "property": "Área",
                        "select": {"equals": area},
                    },
                }
            )
            materias = [Materia(materia) for materia in respuesta["results"]]
            return materias
        except Exception as e:
            logging.error(e)
            return []

    async def consultar_por_materias_del_area_dai(self) -> list[Materia]:
        return await self.consultar_materias_por_area(
            "Diseño de Aplicaciones Informáticas"
        )

    async def consultar_por_materias_del_area_pdc(self) -> list[Materia]:
        return await self.consultar_materias_por_area(
            "Procesamiento Digital y Comunicaciones"
        )

    async def consultar_por_materias_de_tics(self) -> list[Materia]:
        return (
            await self.consultar_por_materias_del_area_dai()
            + await self.consultar_por_materias_del_area_pdc()
        )
