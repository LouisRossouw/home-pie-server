import os
import json
import datetime

import shared.utils.utils as utils

from rest_framework import status
from rest_framework.response import Response

from projects.time_in_progress.socials_calculations.calculations import get_graph_data

from .decorators import decorator_accounts, decorator_account_detail, decorator_overview
from .service import remove_account_from_config, get_all_accounts_from_dir, add_account_to_config


@decorator_accounts
def accounts(request):
    if request.method == 'GET':
        data = get_all_accounts_from_dir()

        return Response({'ok': True, 'data': data})

    if request.method == 'POST':
        account_name = request.data.get('account')
        active = request.data.get('active', True)

        add_account_to_config(account_name, active)

        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_account_detail
def account_detail(request, account_name):

    if request.method == 'GET':

        account = request.GET.get('account') or "time.in.progress"
        platform = request.GET.get('platform') or 'instagram'
        range = request.GET.get('range') or "hour"
        interval = int(request.GET.get('interval') or 1)

        data, historicData = get_graph_data(account, range, interval, platform)

        return Response({'ok': True, 'data': data, "history": historicData}, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        active = request.data.get('active')
        add_account_to_config(account_name, active)
        return Response({'ok': True}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        remove_account_from_config(account_name)
        return Response({'ok': True}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_overview
def overview(request):
    """ Returns current data. """

    if request.method == "GET":
        start_time = utils.start_time()

        accounts = json.loads(request.GET.get('accounts') or [])

        platform = request.GET.get('platform') or 'instagram'
        interval = int(request.GET.get('interval') or 12)
        range = request.GET.get('range') or "hour"

        data_list = []
        history_list = []

        for account in accounts:
            data, historic = get_graph_data(account, range, interval, platform)

            data_list.append(data)
            history_list.append(historic)

        elapsed_time = utils.calculate_DB_time(start_time)

        context = {'ok': True,
                   'datetime': datetime.datetime.now(),
                   'db_elapsed_time': elapsed_time,
                   'current_data': data_list,
                   'historic_data': history_list
                   }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
