import string
import random

def generate_password(length=16, include_special_chars=True, exclude_similar_chars=True):
    """Generate a random secure password."""

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    # Define similar looking characters to exclude
    similar_chars = '0O1l'

    # Combine character sets based on user preferences
    char_set = letters + digits
    if include_special_chars:
        char_set += special_chars
    if exclude_similar_chars:
        char_set = ''.join(char for char in char_set if char not in similar_chars)

    # Generate the password
    password = ''.join(random.choice(char_set) for _ in range(length))

    return password

# Example usage
if __name__ == "__main__":
    print("Generated Password:", generate_password())
