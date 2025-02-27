
from django.conf import settings
import shared.utils.utils as utils
from rest_framework.response import Response
from .decorators import decorator_stats, decorator_health
from shared.utils.printouts.printout_general import printout


F = str(__name__)

SS = {'file': F, "func": "stats"}
HH = {'file': F, "func": "health"}


@decorator_stats
def stats(request):
    start_time = utils.start_time()

    # TODO

    data = {
        'active': True,
    }

    printout(SS)
    utils.calculate_DB_time(start_time)
    return Response(data, status=200)


@decorator_health
def health(request):
    start_time = utils.start_time()

    # TODO

    data = {
        'active': True,
    }

    printout(HH, f"Health Stats:{'todo'}")
    utils.calculate_DB_time(start_time)
    return Response(data, status=200)
