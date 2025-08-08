
import datetime

from rest_framework import status
from rest_framework.response import Response
from .decorators import decorator_overview_data, decorator_start_gengen, decorator_check_genGen_progress

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from .generation import gengen
from .socials_calculations import calculations

F = str(__name__)
OD = {'file': F, "func": "overview_data"}
SG = {'file': F, "func": "start_gengen"}
CGP = {'file': F, "func": "check_genGen_progress"}


@decorator_overview_data
def overview_data(request):
    """ Returns current data. """

    if request.method == "GET":
        start_time = utils.start_time()

        account = request.GET.get('account') or "time.in.progress"
        set_range = request.GET.get('range') or "hour"
        set_length = request.GET.get('interval') or 1

        insta_data, insta_clean = calculations.get_graph_data(
            str(account), str(set_range), int(set_length), 'instagram')

        youtube_data, youtube_clean = calculations.get_graph_data(
            str(account), str(set_range), int(set_length), 'youtube')

        twitter_data, twitter_clean = calculations.get_graph_data(
            str(account), str(set_range), int(set_length), 'x-twitter')

        tiktok_data, tiktok_clean = calculations.get_graph_data(
            str(account), str(set_range), int(set_length), 'tiktok')

        bluesky_data, bluesky_clean = calculations.get_graph_data(
            str(account), str(set_range), int(set_length), 'bluesky')

        printout(OD)
        elapsed_time = utils.calculate_DB_time(start_time)

        context = {
            'ok': True,
            'datetime': datetime.datetime.now(),
            'db_elapsed_time': elapsed_time,
            'instagram': {
                'data': insta_data,
                'history': insta_clean
            },
            'youtube': {
                'data': youtube_data,
                'history': youtube_clean
            },
            'twitter': {
                'data': twitter_data,
                'history': twitter_clean
            },
            'tiktok': {
                'data': tiktok_data,
                'history': tiktok_clean
            },
            'bluesky': {
                'data': bluesky_data,
                'history': bluesky_clean
            }
        }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# ** --- Generate time in progress content.
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
def check_genGen_progress(request):
    """ Returns the current progress of the time in progress content generation. """

    if request.method == "GET":

        printout(CGP)
        progress = gengen.check_gengen()

        return Response({'ok': True, "progress": progress}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- **
