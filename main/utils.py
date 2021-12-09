import random
import string


def get_filename(filename, request):
    return filename.upper()


def random_string_generator(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


