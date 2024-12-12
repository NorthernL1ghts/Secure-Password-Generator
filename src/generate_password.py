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

class EntryPoint:
    @staticmethod
    def Run():
        """Run the password generator with GUI."""
        def generate_passwords():
            try:
                length = int(entry_length.get())
                include_special_chars = var_include_special.get()
                exclude_similar_chars = var_exclude_similar.get()
                include_chars = entry_include_chars.get().strip()
                exclude_chars = entry_exclude_chars.get().strip()

                generator = SecurePasswordGenerator(
                    length=length,
                    exclude_similar_chars=exclude_similar_chars,
                    include_chars=include_chars,
                    exclude_chars=exclude_chars
                )
                passwords = generator.GenerateMultiplePasswords(count=10)
                text_area.delete(1.0, tk.END)
                for pwd in passwords:
                    text_area.insert(tk.END, f"Generated Password: {pwd}\n")

            except ValueError as ve:
                messagebox.showerror("Error", str(ve))

        # Create the main window
        root = tk.Tk()
        root.title("Secure Password Generator")
        root.geometry("600x400")  # Set the window size to be wider

        # Create and place widgets
        tk.Label(root, text="Password Length (12-25):").grid(row=0, column=0, padx=10, pady=5)
        entry_length = tk.Entry(root)
        entry_length.grid(row=0, column=1, padx=10, pady=5)

        var_include_special = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Include Special Characters", variable=var_include_special).grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        var_exclude_similar = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Exclude Similar-looking Characters", variable=var_exclude_similar).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(root, text="Specific Characters to Include (leave blank if none):").grid(row=3, column=0, padx=10, pady=5)
        entry_include_chars = tk.Entry(root)
        entry_include_chars.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Specific Characters to Exclude (leave blank if none):").grid(row=4, column=0, padx=10, pady=5)
        entry_exclude_chars = tk.Entry(root)
        entry_exclude_chars.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(root, text="Generate Passwords", command=generate_passwords).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        text_area = scrolledtext.ScrolledText(root, width=60, height=20)
        text_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Start the GUI event loop
        root.mainloop()

if __name__ == "__main__":
    EntryPoint.Run()
