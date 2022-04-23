from string import ascii_letters as letters
from string import digits as digits
import random

def generate_pass():
    symbols = '!@#$%*&'
    mixture = digits + letters + symbols
    result = ''.join(random.choices(mixture, k=random.randint(8, 12)))
    return result