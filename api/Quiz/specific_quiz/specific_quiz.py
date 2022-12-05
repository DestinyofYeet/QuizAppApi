from api.utils.sql.interface import Interface


class SpecificQuizSection:
    def __init__(self, id_self: int, id_punkt: int, description: str, name: str, coordinates: str, punkt_name: str):
        self.id_self = id_self
        self.id_punkt = id_punkt
        self.description = description
        self.name = name
        self.coordinates = coordinates
        self.punkt_name = punkt_name

    def return_json(self):
        return {
            "id": self.id_self,
            "punkt_id": self.id_punkt,
            "beschreibung": self.description,
            "koordinaten": self.coordinates,
            "punkt_name": self.punkt_name,
            "name": self.name
        }


class SpecificQuiz:
    def __init__(self, name, quizzes: list):
        self.name = name
        self.quizzes: list[SpecificQuizSection] = []

        for quiz in quizzes:
            self.quizzes.append(SpecificQuizSection(*quiz))

    def return_json(self):
        return {
            "name": self.name,
            "parts": [i.return_json() for i in self.quizzes]
        }


def get_quiz(location_name: str) -> SpecificQuiz:
    interface = Interface()

    sql = """select gr_rätsel.id, gr_punkt.id, gr_rätsel.beschreibung, gr_rätsel.name_ort, gr_rätsel.koordinaten, gr_punkt.punkt_name from gr_rätsel
        join (gr_rätsel_punkt as gr_punkt)
        where gr_punkt.punkt_name = %(name)s and gr_punkt.id = gr_rätsel.gr_rätsel_punkt_id"""

    values = {
        "name": location_name
    }

    result = interface.execute(sql, values)

    return SpecificQuiz(location_name, result)
