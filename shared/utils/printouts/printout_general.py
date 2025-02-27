from django.conf import settings
from colorama import Fore, Back, Style, init


def printout(data, extra=""):
    if settings.PRINTOUTS:
        print(Fore.MAGENTA, f"🔹{data.get('file')} | {data.get('func')}:", Style.RESET_ALL,
              extra,  Style.RESET_ALL)
