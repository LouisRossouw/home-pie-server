from rest_framework import status
from rest_framework.response import Response
from .decorators import decorator_start_gengen, decorator_check_genGen_progress

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from .generation import gengen


F = str(__name__)
SG = {'file': F, "func": "start_gengen"}
CGP = {'file': F, "func": "check_genGen_progress"}


@decorator_start_gengen
def start_gengen(request):
    """ Starts the content generation process for time in progress. """

    if request.method == "POST":
        start_time = utils.start_time()

        printout(SG)
        hasStarted = gengen.run_gengen()

        utils.calculate_DB_time(start_time)
        return Response({'ok': True, 'hasStarted': hasStarted}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_check_genGen_progress
def check_progress(request):
    """ Returns the current progress of the time in progress content generation. """

    if request.method == "GET":

        printout(CGP)
        progress = gengen.check_gengen()

        return Response({'ok': True, "progress": progress}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
