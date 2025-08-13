
import datetime

from rest_framework import status
from rest_framework.response import Response
from .decorators import decorator_overview

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from .socials_calculations import calculations

F = str(__name__)
OD = {'file': F, "func": "overview_data"}


@decorator_overview
def overview(request):
    """ Returns current data. """

    if request.method == "GET":
        start_time = utils.start_time()

        account = request.GET.get('account') or "time.in.progress"
        range = request.GET.get('range') or "hour"
        interval = request.GET.get('interval') or 1

        insta_data, insta_clean = calculations.get_graph_data(
            str(account), str(range), int(interval), 'instagram')

        youtube_data, youtube_clean = calculations.get_graph_data(
            str(account), str(range), int(interval), 'youtube')

        twitter_data, twitter_clean = calculations.get_graph_data(
            str(account), str(range), int(interval), 'x-twitter')

        tiktok_data, tiktok_clean = calculations.get_graph_data(
            str(account), str(range), int(interval), 'tiktok')

        bluesky_data, bluesky_clean = calculations.get_graph_data(
            str(account), str(range), int(interval), 'bluesky')

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
