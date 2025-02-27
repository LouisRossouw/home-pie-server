from django.conf import settings
from colorama import Fore, Back, Style, init


def printout_is_authenticated(frm, fn, is_auth, email, id, is_staff):
    if settings.PRINTOUTS:
        if is_auth:
            color = Fore.YELLOW
        else:
            color = Fore.LIGHTYELLOW_EX
        if is_staff:
            staff_color = Fore.BLUE
        else:
            staff_color = Fore.YELLOW
        print(color, f"🔹{frm} | {fn}:", Style.RESET_ALL, 'Auth:', Fore.GREEN, email,
              Style.RESET_ALL, ', ID:', Fore.BLUE, id,  Style.RESET_ALL, 'is_staff:', staff_color, is_staff, Style.RESET_ALL, '')
