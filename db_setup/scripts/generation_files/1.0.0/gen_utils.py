import random
import string

def get_random_string(min_length, max_length):
    if min_length == max_length:
        length = min_length
    else:
        length = random.randint(min_length, max_length)
    letters = string.ascii_letters + string.digits + ' '
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string