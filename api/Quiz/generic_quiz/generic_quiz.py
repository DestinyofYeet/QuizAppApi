import ast

from api.utils.sql.interface import Interface


def get_quiz():
    interface = Interface()

    sql = "select * from simple_quizzes order by RAND() limit 1;"
    result = interface.execute(sql)

    return Quiz(*result[0])


class Quiz:
    def __init__(self, q_id, question, possible_answers, correct_answers, added_by):
        self.id: int = q_id
        self.question: str = question
        self.possible_answers: list[str] = ast.literal_eval(possible_answers)
        self.correct_answer: str = correct_answers
        self.added_by = added_by

    def return_json(self):
        self.possible_answers = [str(i) for i in self.possible_answers]
        return {
            "id": self.id,
            "question": self.question,
            "possible_answers": self.possible_answers,
            "correct_answer": str(self.correct_answer)
        }
