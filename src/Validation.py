import re

class Validation:
    @staticmethod
    def ValidateLength(length):
        if not 12 <= length <= 25:
            raise ValueError("Password length must be between 12 and 25 characters.")

    @staticmethod
    def HasRepeatingCharacters(password):
        return re.search(r'(.)\1', password)
