
from django.conf import settings
import shared.utils.utils as utils
from rest_framework.response import Response
from .decorators import decorator_stats, decorator_health, decorator_test_view, decorator_home_view
from shared.utils.printouts.printout_general import printout


F = str(__name__)

HV = {'file': F, "func": "home_view"}
SS = {'file': F, "func": "stats"}
HH = {'file': F, "func": "health"}
TV = {'file': F, "func": "test_view"}

@decorator_home_view
def home_view(request):
    start_time = utils.start_time()
    printout(HV)
    utils.calculate_DB_time(start_time)
    return Response({"message": "Welcome to Home Pie API"}, status=200)

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

@decorator_test_view
def test_view(request):
    start_time = utils.start_time()

    print('😀 Called test view')
    response = {
        'message': 'This is just a test response.'
    }

    printout(SS)
    utils.calculate_DB_time(start_time)
    return Response(response, status=200)