import time
import random
import string

from colorama import Fore, Back, Style, init

def start_time():
    return time.time()


def calculate_DB_time(start_time):
    elapsed_time = time.time() - start_time
    print(Fore.YELLOW, 'DB time: ', elapsed_time, Style.RESET_ALL)


def generate_random_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_invoice(user_name):
    unique_id = f"{str(user_name)}_{str(random.randint(1, 10000000000))}"
    return unique_id