import string
import random
import re

def generate_password(length=16, include_special_chars=True, exclude_similar_chars=True):
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

    # Ensure password is strong or excellent
    while True:
        password = ''.join(random.choice(char_set) for _ in range(length))
        if (re.search(r'[a-z]', password) and re.search(r'[A-Z]', password) and
                re.search(r'[0-9]', password) and (not include_special_chars or re.search(r'[!@#$%^&*(),.?":{}|<>]', password))):
            # Ensure no repeating characters next to each other
            if not re.search(r'(.)\1', password):
                break

    return password

# Example usage
if __name__ == "__main__":
    try:
        print("Generated Password:", generate_password(length=16))
    except ValueError as ve:
        print(ve)
