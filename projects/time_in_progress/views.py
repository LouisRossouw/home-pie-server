
import datetime

from rest_framework import status
from rest_framework.response import Response
from .decorators import decorator_overview_data

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from .socials_calculations import instagram
from .socials_calculations import youtube
from .socials_calculations import tiktok
from .socials_calculations import twitter
from .socials_calculations import bluesky

F = str(__name__)
OD = {'file': F, "func": "overview_data"}


@decorator_overview_data
def overview_data(request):
    """ Returns current data. """

    if request.method == "GET":
        start_time = utils.start_time()

        account = request.GET.get('account') or "time.in.progress"
        set_range = request.GET.get('set_range') or "hours"
        set_length = request.GET.get('set_length') or 1

        insta_data, insta_clean = instagram.get_difference(
            str(account), str(set_range), int(set_length))

        youtube_data, youtube_clean = youtube.get_difference(
            str(account), str(set_range), int(set_length))

        twitter_data, twitter_clean = twitter.get_difference(
            str(account), str(set_range), int(set_length))

        tiktok_data, tiktok_clean = tiktok.get_difference(
            str(account), str(set_range), int(set_length))

        bluesky_data, bluesky_clean = bluesky.get_difference(
            str(account), str(set_range), int(set_length))

        context = {'ok': True,
                   'datetime': datetime.datetime.now(),
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
        printout(OD)

        utils.calculate_DB_time(start_time)
        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
