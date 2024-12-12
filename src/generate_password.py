import string
import random
import re
import os

def generate_password(length=16, include_special_chars=True, exclude_similar_chars=True, min_digits=1, min_special=1):
    """Generate a random secure password with specific rules."""

    if not 8 < length < 25:
        raise ValueError("Password length must be more than 8 and less than 25 characters.")

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    similar_chars = '0O1l'

    # Combine character sets based on user preferences
    char_set = letters + digits
    if include_special_chars:
        char_set += special_chars
    if exclude_similar_chars:
        char_set = ''.join(char for char in char_set if char not in similar_chars)

    # Ensure password meets the specified rules
    while True:
        password = ''.join(random.choice(char_set) for _ in range(length))

        if (re.search(r'[a-z]', password) and re.search(r'[A-Z]', password) and
                re.search(r'[0-9]', password) and (not include_special_chars or re.search(r'[!@#$%^&*(),.?":{}|<>]', password)) and
                len(re.findall(r'[0-9]', password)) >= min_digits and
                len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) >= min_special and
                not re.search(r'(.)\1', password)):
            break

    return password

def save_passwords_to_file(passwords, directory="../out", filename="passwords.txt"):
    """Save the generated passwords to a file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as file:
        for password in passwords:
            file.write(f"Generated Password: {password}\n")
    print(f"Passwords saved to {filepath}")

def generate_multiple_passwords(count=1, length=16, include_special_chars=True, exclude_similar_chars=True, min_digits=1, min_special=1):
    """Generate multiple passwords and save them to a file."""
    passwords = [generate_password(length, include_special_chars, exclude_similar_chars, min_digits, min_special) for _ in range(count)]
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
