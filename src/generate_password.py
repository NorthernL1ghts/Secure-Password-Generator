import string
import random
import re
import os
import time
from secrets import SystemRandom
import tkinter as tk
from tkinter import messagebox, scrolledtext

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
        if self.m_IncludeChars:
            char_set += self.m_IncludeChars
        if self.m_ExcludeChars:
            char_set = ''.join(char for char in char_set if char not in self.m_ExcludeChars)

        # Ensure minimum counts of each character type
        password = (
            [self.m_SecureRandom.choice(letters_upper) for _ in range(self.m_MinUppercase)] +
            [self.m_SecureRandom.choice(letters_lower) for _ in range(self.m_MinLowercase)] +
            [self.m_SecureRandom.choice(digits) for _ in range(self.m_MinDigits)] +
            [self.m_SecureRandom.choice(special_chars) for _ in range(self.m_MinSpecial)]
        )

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

    def GenerateMultiplePasswords(self, count=10):
        """Generate multiple passwords and save them to a file."""
        passwords = [self.GeneratePassword() for _ in range(count)]
        return passwords

class Window:
    def __init__(self, root):
        self.m_Root = root
        self.m_Root.title("Secure Password Generator")
        self.m_Root.geometry("600x400")  # Set the window size to be wider

        self.CreateWidgets()

    def CreateWidgets(self):
        # Create and place widgets
        tk.Label(self.m_Root, text="Password Length (12-25):").grid(row=0, column=0, padx=10, pady=5)
        self.m_EntryLength = tk.Entry(self.m_Root)
        self.m_EntryLength.grid(row=0, column=1, padx=10, pady=5)

        self.m_VarIncludeSpecial = tk.BooleanVar(value=True)
        tk.Checkbutton(self.m_Root, text="Include Special Characters", variable=self.m_VarIncludeSpecial).grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.m_VarExcludeSimilar = tk.BooleanVar(value=True)
        tk.Checkbutton(self.m_Root, text="Exclude Similar-looking Characters", variable=self.m_VarExcludeSimilar).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(self.m_Root, text="Specific Characters to Include (leave blank if none):").grid(row=3, column=0, padx=10, pady=5)
        self.m_EntryIncludeChars = tk.Entry(self.m_Root)
        self.m_EntryIncludeChars.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.m_Root, text="Specific Characters to Exclude (leave blank if none):").grid(row=4, column=0, padx=10, pady=5)
        self.m_EntryExcludeChars = tk.Entry(self.m_Root)
        self.m_EntryExcludeChars.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.m_Root, text="Generate Passwords", command=self.GeneratePasswords).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.m_TextArea = scrolledtext.ScrolledText(self.m_Root, width=60, height=20)
        self.m_TextArea.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def GeneratePasswords(self):
        try:
            length = int(self.m_EntryLength.get())
            include_special_chars = self.m_VarIncludeSpecial.get()
            exclude_similar_chars = self.m_VarExcludeSimilar.get()
            include_chars = self.m_EntryIncludeChars.get().strip()
            exclude_chars = self.m_EntryExcludeChars.get().strip()

            generator = SecurePasswordGenerator(
                length=length,
                exclude_similar_chars=exclude_similar_chars,
                include_chars=include_chars,
                exclude_chars=exclude_chars
            )
            passwords = generator.GenerateMultiplePasswords(count=10)
            self.m_TextArea.delete(1.0, tk.END)
            for pwd in passwords:
                self.m_TextArea.insert(tk.END, f"Generated Password: {pwd}\n")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

class EntryPoint:
    @staticmethod
    def Run():
        """Run the password generator with GUI."""
        root = tk.Tk()
        window = Window(root)
        root.mainloop()

if __name__ == "__main__":
    EntryPoint.Run()
