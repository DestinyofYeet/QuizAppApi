class QuizType:
    generic = "generic"
    specific = "specific"

    @staticmethod
    def from_string(string):
        for var in vars(QuizType):
            if var == string:
                return var

        return None
