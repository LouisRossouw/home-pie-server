import shared.utils.utils as utils
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys
sys.path.append(".")

load_dotenv()


data_path = os.getenv('DATA_DIR')
data_dir = os.path.join(data_path, "x-twitter")


def get_all_accounts():

    accounts = os.listdir(data_dir)
    accounts_List = []

    for account in accounts:
        account_path = os.path.join(data_dir, account)
        if account != ".gitignore":
            accounts_List.append(account)

    return accounts_List


def get_graph_data(account, set_range, set_length):
    """ Returns data for the graph """

    account_data_dir = os.path.join(data_dir, account)

    data_range = filter_range(set_range, set_length)
    data_list = get_account_data_list(account_data_dir)
    chosen_data = get_files_from_range(data_list, account_data_dir, data_range)

    clean = []
    collection = []
    follower_count = []

    # Get the earliest dates / times based on the set length.
    for data_date in chosen_data:
        data = utils.read_json(data_date)

        for key, value in data.items():
            try:
                time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(key, "%Y-%m-%d")

        name = value["name"]
        post_value = int(value["stats"]["tweets_value"])
        followers_value = int(value["stats"]["followers_value"])

        start_time = go_back_time(time, set_range, set_length)
        time_difference = time - start_time

    # Get the the latest data.
    no_duplicates_list = []

    for data_date in chosen_data:
        data = utils.read_json(data_date)
        print('- - - -')
        prev_data = 10
        prev_post = None
        for prev, prev_value in data.items():
            try:
                time = datetime.strptime(prev, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(prev, "%Y-%m-%d")

            if start_time <= time:

                past_name = prev_value["name"]
                date = prev
                past_post_value = int(prev_value["stats"]["tweets_value"])
                past_followers_value = int(
                    prev_value["stats"]["followers_value"])

                # Append when posted a new post.
                if past_post_value != prev_post and prev_post != None:
                    posted_at_followers_count = past_followers_value
                else:
                    posted_at_followers_count = 0
                prev_post = past_post_value

                collection.append({prev: prev_value})
                follower_count.append(past_followers_value)

                value_data = maybe_append(date, set_range,  set_length)

                percent = (int(prev_data) / int(past_followers_value)) * 100
                growth = 100 - percent
                prev_data = past_followers_value

                if growth < 80:
                    if value_data not in no_duplicates_list:
                        no_duplicates_list.append(value_data)

                        clean.append({
                            'name': past_name,
                            'post': past_post_value,
                            'followers': past_followers_value,
                            'date': date,
                            'postedAt': posted_at_followers_count
                        })

                        # print(value_data, past_followers_value)
                        # print(time.strftime("%Y-%m-%d %H:%M"), "| diff:", time - start_time, " | ",
                        # int(past_followers_value),'-', int(followers_value), "=",
                        # int(followers_value) - int(past_followers_value))

        print('- - - -')


def get_account_data_list(account_path):
    sorted_list = None
    if os.path.isdir(account_path):
        data_list = os.listdir(account_path)

        # Sort based on the integer part before the underscore
        sorted_list = sorted(data_list, key=lambda x: int(x.split('_')[0]))

    return sorted_list


def filter_range(filter_by, set_length):
    """ Returns all the data for specific month if exists. """

    # setting_range = "minutes" # "minutes", "hourly", "days", "weeks", "months", "years", "custom"
    setting_range = filter_by
    default_minutes = 20
    default_hours = 1
    default_days = 1
    default_weeks = 1
    default_months = 30
    default_years = 365

    search_from = ""
    search_to = current_datetime = datetime.now()

    if setting_range == "minutes":
        search_from = current_datetime - timedelta(minutes=set_length)

    if setting_range == "hours":
        search_from = current_datetime - timedelta(hours=set_length)

    if setting_range == "days":
        search_from = current_datetime - timedelta(days=set_length)

    if setting_range == "weeks":
        search_from = current_datetime - timedelta(weeks=set_length)

    if setting_range == "months":
        search_from = current_datetime - timedelta(days=set_length)

    if setting_range == "years":
        search_from = current_datetime - timedelta(days=set_length)

    if setting_range == "custom":
        print("todo")

    day_number = f"{search_from.day:02}"
    month_name = search_from.strftime("%B")
    year_number = search_from.strftime("%Y")

    print(day_number, month_name, year_number)

    data = {
        "day_number": day_number,
        "month_name": month_name,
        "year_number": year_number,
        "search_from": search_from,
        "search_to": search_to
    }

    return data


def go_back_time(time, time_type, amount):

    if time_type == "minutes":
        search_from = time - timedelta(minutes=amount)

    if time_type == "hours":
        search_from = time - timedelta(hours=amount)

    if time_type == "days":
        search_from = time - timedelta(days=amount)

    if time_type == "weeks":
        search_from = time - timedelta(weeks=amount)

    if time_type == "months":
        search_from = time - timedelta(days=amount)

    if time_type == "years":
        search_from = time - timedelta(days=amount)

    if time_type == "custom":
        print("todo")

    return search_from


def get_files_from_range(data_list, account_data_dir, data_range):

    chosen_index = len(data_list)
    data_length = len(data_list)

    for data in data_list:
        file_name = data.split('.')[0]
        index, year, month = file_name.split('_')

        if data_range["month_name"] == month:
            if data_range["year_number"] == year:
                file = os.path.join(account_data_dir, data)

                if os.path.exists(file):
                    chosen_index = int(index)

    chosen_data = []

    if chosen_index != data_length:
        for i in range(chosen_index, data_length + 1):
            chosen_data.append(os.path.join(
                account_data_dir, data_list[i - 1]))

    if chosen_index == data_length:
        chosen_data.append(os.path.join(account_data_dir, data_list[-1]))

    if not chosen_data:
        chosen_data.append(os.path.join(account_data_dir, data_list[-1]))

    return chosen_data


def calculate_average_difference(list_of_values):

    # Calculate the differences between consecutive numbers
    differences = [list_of_values[i] - list_of_values[i - 1]
                   for i in range(1, len(list_of_values))]

    # Calculate the sum of differences
    total_difference = sum(differences)

    # Calculate the average difference
    if total_difference != 0:
        average_difference = total_difference / len(differences)
    else:
        average_difference = 0

    return round(average_difference, 2)


def maybe_append(date, set_range, set_length):

    append_value = date

    try:
        datetime_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        datetime_object = datetime.strptime(
            date + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

    if set_range == "hours" and set_length > 6:
        value = datetime_object.hour
        day = datetime_object.day
        append_value = str(day) + '_' + str(value)

    if set_range == "days":
        if set_length > 1:
            day = datetime_object.day
            month = datetime_object.month
            append_value = str(month) + '_' + str(day)
        if set_length == 1:
            value = datetime_object.hour
            day = datetime_object.day
            append_value = str(day) + '_' + str(value)

    return append_value


def get_difference(account, set_range, set_length):

    account_data_dir = os.path.join(data_dir, account)

    data_range = filter_range(set_range, set_length)
    data_list = get_account_data_list(account_data_dir)
    chosen_data = get_files_from_range(data_list, account_data_dir, data_range)

    clean = []
    collection = []
    follower_count = []

    # Get the earliest dates / times based on the set length.
    for data_date in chosen_data:
        data = utils.read_json(data_date)

        for key, value in data.items():
            try:
                time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(
                    key + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

        name = value["name"]
        post_value = int(value["stats"]["tweets_value"])
        followers_value = int(value["stats"]["followers_value"])

        start_time = go_back_time(time, set_range, set_length)
        time_difference = time - start_time

    # Get the the latest data.
    no_duplicates_list = []
    for data_date in chosen_data:
        data = utils.read_json(data_date)
        print('- - - -')
        prev_data = 10
        prev_post = None
        for prev, prev_value in data.items():
            try:
                time = datetime.strptime(prev, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(
                    prev + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

            if start_time <= time:

                past_name = prev_value["name"]
                date = prev
                past_post_value = int(prev_value["stats"]["tweets_value"])
                past_followers_value = int(
                    prev_value["stats"]["followers_value"])

                collection.append({prev: prev_value})
                follower_count.append(past_followers_value)

                value_data = maybe_append(date, set_range,  set_length)

                percent = (int(prev_data) / int(past_followers_value)) * 100
                growth = 100 - percent
                prev_data = past_followers_value

                if growth < 80:

                    if value_data not in no_duplicates_list:
                        no_duplicates_list.append(value_data)

                        # Append when posted a new post.
                        if past_post_value != prev_post and prev_post != None:
                            print('yeaaah', past_followers_value)
                            posted_at_followers_count = past_followers_value
                        else:
                            posted_at_followers_count = None
                        prev_post = past_post_value

                        clean.append({
                            'name': past_name,
                            'post': past_post_value,
                            'followers': past_followers_value,
                            'date': date,
                            'postedAt': posted_at_followers_count
                        })

                        print(time.strftime("%Y-%m-%d %H:%M"), "| diff:", time - start_time, " | ",
                              int(past_followers_value), '-', int(followers_value), "=",
                              int(followers_value) - int(past_followers_value))

        print('- - - -')

    # Compare data between the from and the to.
    prev_time = collection[0]

    for t in prev_time:

        name = prev_time[t]["name"]
        past_post_value = int(prev_time[t]["stats"]["tweets_value"])
        past_followers_value = int(prev_time[t]["stats"]["followers_value"])

        try:
            t_date = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            t_date = datetime.strptime(
                t + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

        post_difference = int(post_value) - int(past_post_value)
        followers_difference = int(followers_value) - int(past_followers_value)
        print('\nSummary:')
        print("From:", t_date.strftime("%Y-%m-%d %H:%M"),
              "to:", time.strftime("%Y-%m-%d %H:%M"))

        avarage_per_10_min = calculate_average_difference(follower_count)

        print(
            "Range:", set_range,
            "Set Length:", set_length, '=',
            time_difference, "|",
            int(past_followers_value), '-',
            int(followers_value), '=',
            followers_difference,
            'Followers', '\nAverage difference per +- 10 min:',
            avarage_per_10_min,
            '\nAverage difference per +- 1 hour:',
            round(avarage_per_10_min * 6, 2),
            '\nAverage difference per +- 1 day:',
            round(avarage_per_10_min * 24, 2),
            '\nAverage difference per +- 1 week:',
            round(avarage_per_10_min * (24 * 7), 2),
            '\nAverage difference per +- 1 month:',
            round(avarage_per_10_min * (24 * 30), 2),
        )
        print('*')

        data = {
            "account": account,

            "to_date": time,
            "latest_post_value": int(post_value),
            "latest_followers": int(followers_value),

            "from_date": t_date,
            "past_post_value": int(past_followers_value),
            "past_followers_value": past_followers_value,

            "post_difference": post_difference,
            "followers_difference": followers_difference,

            "avarage_per_10_min": avarage_per_10_min,
            "avarage_per_1_hour": round(avarage_per_10_min * 6, 2),
            "avarage_per_1_day": round(avarage_per_10_min * 24, 2),
            "avarage_per_1_week": round(avarage_per_10_min * (24 * 7), 2),
            "avarage_per_1_month": round(avarage_per_10_min * (24 * 30), 2),
        }

    return data, clean


if __name__ == "__main__":

    set_range = "hours"
    set_length = 1

    account = "time.in.progress"
    # account = "progressbar_"
    # account = "rockettotheskies"
    # account = "arcadestudio"

    # data_dir = "//DESKTOP-NGJ1BOP/Projects/Insta-Progress/data"

    # data = get_difference(account, set_range, set_length)

    get_graph_data(account, "hours", 24)
