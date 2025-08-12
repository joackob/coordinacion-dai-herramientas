import tqdm
import random
from pprint import pprint
from src.bases_de_datos_en_notion.bdd import BDD


class Estudiantes(BDD):
    _iconos = [
        "😊",
        "😃",
        "😄",
        "😁",
        "😎",
        "🥳",
        "🤩",
        "😺",
        "🎈",
        "🌟",
        "🎉",
        "🍀",
        "🦄",
        "🌈",
        "💖",
        "🐣",
        "🍭",
        "🧸",
        "🏅",
        "⚽",
    ]

    async def cargar_estudiante(self, nombre_completo: str, comision: str):
        try:
            await self._notion_client.pages.create(
                parent={"database_id": self._database_id},
                properties={
                    "Name": {  # Asegúrate de que "Name" coincida con el nombre de la propiedad principal en tu base de datos
                        "title": [{"text": {"content": f"{nombre_completo}"}}]
                    },
                    "Comisión": {"select": {"name": comision}},
                },
                icon={
                    "type": "emoji",
                    "emoji": f"{random.choice(self._iconos)}",
                },
            )
            return self
        except Exception as e:
            pprint(e)
            raise Exception(f"Error al crear la página para {nombre_completo}")


class EstudiantesABP5to(Estudiantes):
    _estudiantes_comision_d = [
        # 5to D
        "Diego Ledezma",
        "Nain Isla",
        "Joaquin Pirilio",
        "Lian Leyenda",
        "Ayelen Quispe",
        "Ariana Villa",
        "Enzo Materazzi",
        "Valentin Velazquez",
        "Rocio Albarracin",
        "Evelyn Villarreal",
        "Abril Herbas",
        "Lucia Acuña",
        "Llusco Mary",
        "Dylan Aragon",
        "Santiago Bunzolino",
        "Juan Manuel Parrado",
        "Fernando Valle",
        "Avila Tomas",
    ]
    _estudiantes_comision_b = [
        # 5to B
        "Sol Perez",
        "Ana Cristina",
        "Julieta Mendoza",
        "Bautista Moyano",
        "Thiago Gomez",
        "Miguel Angel Diaz",
        "Leonardo Ojeda",
        "Karen Diaz",
        "Luana Lopez",
        "Priscila dellatore",
        "Luciano Alcaraz",
        "Gabriel",
        "Luciano Savia",
        "Briseida Uscamayta",
        "Brigit Aguirre",
        "Joel Agustin",
    ]


class EstudantesABP5toCLI(EstudiantesABP5to):

    async def cargar_y_mostrar_progreso(self):
        for estudiante in tqdm.tqdm(
            self._estudiantes_comision_d,
            desc="Cargando estudiantes 5to D",
        ):
            await self.cargar_estudiante(estudiante, comision="5to D")

        for estudiante in tqdm.tqdm(
            self._estudiantes_comision_b,
            desc="Cargando estudiantes 5to B",
        ):
            await self.cargar_estudiante(estudiante, comision="5to B")

        return self
