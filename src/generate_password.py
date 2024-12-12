import string
import random
import re
import os
from secrets import SystemRandom

class SecurePasswordGenerator:
    def __init__(self, length=16, min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1, exclude_similar_chars=True):
        self.m_Length = length
        self.m_MinUppercase = min_uppercase
        self.m_MinLowercase = min_lowercase
        self.m_MinDigits = min_digits
        self.m_MinSpecial = min_special
        self.b_ExcludeSimilarChars = exclude_similar_chars
        self.m_SecureRandom = SystemRandom()

    def GeneratePassword(self):
        """Generate a random secure password with specific rules."""

        if not 12 <= self.m_Length <= 25:
            raise ValueError("Password length must be between 12 and 25 characters.")

        # Define character sets
        letters_upper = string.ascii_uppercase
        letters_lower = string.ascii_lowercase
        digits = string.digits
        special_chars = string.punctuation
        similar_chars = '0O1l'

        # Combine character sets based on user preferences
        char_set = letters_upper + letters_lower + digits + special_chars
        if self.b_ExcludeSimilarChars:
            char_set = ''.join(char for char in char_set if char not in similar_chars)

        # Ensure minimum counts of each character type
        password = (
            [self.m_SecureRandom.choice(letters_upper) for _ in range(self.m_MinUppercase)] +
            [self.m_SecureRandom.choice(letters_lower) for _ in range(self.m_MinLowercase)] +
            [self.m_SecureRandom.choice(digits) for _ in range(self.m_MinDigits)] +
            [self.m_SecureRandom.choice(special_chars) for _ in range(self.m_MinSpecial)]
        )

        # Fill the remaining length with random choices from the char_set
        remaining_length = self.m_Length - len(password)
        password += [self.m_SecureRandom.choice(char_set) for _ in range(remaining_length)]

        # Shuffle the password list to ensure random distribution
        self.m_SecureRandom.shuffle(password)

        password_str = ''.join(password)

        # Ensure no repeating characters next to each other
        if re.search(r'(.)\1', password_str):
            return self.GeneratePassword()

        return password_str

    def SavePasswordsToFile(self, passwords, directory="../out", filename="passwords.txt"):
        """Save the generated passwords to a file."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)

        with open(filepath, 'w') as file:
            for password in passwords:
                file.write(f"Generated Password: {password}\n")
        print(f"Passwords saved to {filepath}")

    def GenerateMultiplePasswords(self, count=1):
        """Generate multiple passwords and save them to a file."""
        passwords = [self.GeneratePassword() for _ in range(count)]
        for pwd in passwords:
            print(f"Generated Password: {pwd}")
        self.SavePasswordsToFile(passwords)

class EntryPoint:
    @staticmethod
    def Run():
        """Run the password generator."""
        try:
            generator = SecurePasswordGenerator(length=16)
            print(f"Generated Password: {generator.GeneratePassword()}")
            generator.GenerateMultiplePasswords(count=5)
        except ValueError as ve:
            print(ve)

if __name__ == "__main__":
    EntryPoint.Run()
