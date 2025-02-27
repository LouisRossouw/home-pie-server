from django.conf import settings
from colorama import Fore, Back, Style, init


def printout_get_user(frm, fn, user):
    if settings.PRINTOUTS:
        print(Fore.MAGENTA, f"🔹{frm} | {fn}:", Style.RESET_ALL, 'User:', Fore.GREEN, user,
              Style.RESET_ALL, )
