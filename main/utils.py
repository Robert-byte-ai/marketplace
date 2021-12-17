from django.core.exceptions import ValidationError
import random
import string

ERROR = ValidationError('ИНН не корректно')


def get_filename(filename, request):
    return filename.upper()


def random_string_generator(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def check_inn(inn):
    if len(inn) not in (10, 12):
        raise ERROR

    def inn_csum(inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11-len(inn):], [int(x) for x in inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) == 10 and inn[-1] == inn_csum(inn[:-1]):
        raise ERROR
    elif inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1]):
        raise ERROR
