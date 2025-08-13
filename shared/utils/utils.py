import time
import json
import random
import string
import datetime
import calendar

from colorama import Fore, Back, Style, init


def start_time():
    return time.time()


def calculate_DB_time(start_time):
    elapsed_time = time.time() - start_time
    print(Fore.YELLOW, 'DB time: ', elapsed_time, Style.RESET_ALL)
    return elapsed_time


def generate_random_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)


def read_json(json_path):
    """ Reads json file """

    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)


def get_dates():
    """ Returns a lot of date stuff! """

    return {'date_now':  (str(datetime.datetime.now()).split(' ')[0]),  # 2024-06-22
            # 00:23:02.199620
            'date_time': (str(datetime.datetime.now()).split(' ')[1]),
            'day_num': datetime.datetime.today().day,
            'day_name': calendar.day_name[datetime.date.today().weekday()],
            'date_year':  datetime.datetime.today().year,
            'day_month_num':  datetime.datetime.today().month,
            'day_month_name': calendar.month_name[datetime.datetime.today().month],
            'date_now_full': datetime.datetime.now(),
            'current_time': datetime.datetime.now().time()
            }
