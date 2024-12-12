import string
import random
import os
import time
from secrets import SystemRandom
from Validation import Validation

class SecurePasswordGenerator:
    def __init__(self, length=16, min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1, exclude_similar_chars=True, include_chars="", exclude_chars=""):
        self.m_Length = length
        self.m_MinUppercase = min_uppercase
        self.m_MinLowercase = min_lowercase
        self.m_MinDigits = min_digits
        self.m_MinSpecial = min_special
        self.b_ExcludeSimilarChars = exclude_similar_chars
        self.m_IncludeChars = include_chars
        self.m_ExcludeChars = exclude_chars
        self.m_SecureRandom = SystemRandom()
        self.m_Validator = Validation()

    def GeneratePassword(self):
        """Generate a random secure password with specific rules."""

        self.m_Validator.ValidateLength(self.m_Length)

        # Define character sets
        letters_upper = string.ascii_uppercase
        letters_lower = string.ascii_lowercase
        digits = string.digits
        special_chars = string.punctuation
        similar_chars = '0O1l'

        # Combine character sets based on user preferences
        char_set = letters_upper + letters_lower + digits
        if self.m_IncludeChars:
            char_set += self.m_IncludeChars
        if not self.m_IncludeChars and not self.m_ExcludeChars:
            char_set += special_chars
        if self.b_ExcludeSimilarChars:
            char_set = ''.join(char for char in char_set if char not in similar_chars)
        if self.m_ExcludeChars:
            char_set = ''.join(char for char in char_set if char not in self.m_ExcludeChars)

        # Ensure minimum counts of each character type
        password = (
            [self.m_SecureRandom.choice(letters_upper) for _ in range(self.m_MinUppercase)] +
            [self.m_SecureRandom.choice(letters_lower) for _ in range(self.m_MinLowercase)] +
            [self.m_SecureRandom.choice(digits) for _ in range(self.m_MinDigits)]
        )
        if self.m_IncludeChars:
            password += [self.m_SecureRandom.choice(self.m_IncludeChars) for _ in range(self.m_MinSpecial)]

        # Fill the remaining length with random choices from the char_set
        remaining_length = self.m_Length - len(password)

        # Add more entropy by seeding with the current time and random OS data
        seed = int(time.time() * 1000)
        seed ^= os.getpid()
        seed ^= random.randint(0, 2**32)
        self.m_SecureRandom.seed(seed)

        password += [self.m_SecureRandom.choice(char_set) for _ in range(remaining_length)]

        # Shuffle the password list to ensure random distribution
        self.m_SecureRandom.shuffle(password)

        password_str = ''.join(password)

        # Ensure no repeating characters next to each other
        if self.m_Validator.HasRepeatingCharacters(password_str):
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

    def GenerateMultiplePasswords(self, count=10):
        """Generate multiple passwords and save them to a file."""
        passwords = [self.GeneratePassword() for _ in range(count)]
        return passwords
