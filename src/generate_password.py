import string
import random
import re
import os
from secrets import SystemRandom

# Secure random number generator
secure_random = SystemRandom()

def generate_password(length=16, min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1, exclude_similar_chars=True):
    """Generate a random secure password with specific rules."""

    if not 12 <= length <= 25:
        raise ValueError("Password length must be between 12 and 25 characters.")

    # Define character sets
    letters_upper = string.ascii_uppercase
    letters_lower = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation
    similar_chars = '0O1l'

    # Combine character sets based on user preferences
    char_set = letters_upper + letters_lower + digits + special_chars
    if exclude_similar_chars:
        char_set = ''.join(char for char in char_set if char not in similar_chars)

    # Ensure minimum counts of each character type
    password = (
        [secure_random.choice(letters_upper) for _ in range(min_uppercase)] +
        [secure_random.choice(letters_lower) for _ in range(min_lowercase)] +
        [secure_random.choice(digits) for _ in range(min_digits)] +
        [secure_random.choice(special_chars) for _ in range(min_special)]
    )

    # Fill the remaining length with random choices from the char_set
    remaining_length = length - len(password)
    password += [secure_random.choice(char_set) for _ in range(remaining_length)]

    # Shuffle the password list to ensure random distribution
    secure_random.shuffle(password)

    password_str = ''.join(password)

    # Ensure no repeating characters next to each other
    if re.search(r'(.)\1', password_str):
        return generate_password(length, min_uppercase, min_lowercase, min_digits, min_special, exclude_similar_chars)

    return password_str

def save_passwords_to_file(passwords, directory="../out", filename="passwords.txt"):
    """Save the generated passwords to a file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as file:
        for password in passwords:
            file.write(f"Generated Password: {password}\n")
    print(f"Passwords saved to {filepath}")

def generate_multiple_passwords(count=1, length=16, min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1, exclude_similar_chars=True):
    """Generate multiple passwords and save them to a file."""
    passwords = [generate_password(length, min_uppercase, min_lowercase, min_digits, min_special, exclude_similar_chars) for _ in range(count)]
    for pwd in passwords:
        print(f"Generated Password: {pwd}")
    save_passwords_to_file(passwords)

# Example usage
if __name__ == "__main__":
    try:
        print(f"Generated Password: {generate_password(length=16)}")
        generate_multiple_passwords(count=5, length=16)
    except ValueError as ve:
        print(ve)
