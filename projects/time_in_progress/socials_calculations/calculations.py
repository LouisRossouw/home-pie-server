import os
from datetime import datetime, timedelta
import shared.utils.utils as utils

data_path = os.getenv('DATA_DIR')


def get_graph_data(account, set_range, set_length, platform):
    """ Returns the accounts historic data """

    post_key, followers_key = get_keys(platform)

    data_dir = os.path.join(data_path, platform)
    account_data_dir = os.path.join(data_dir, account)

    if not os.path.exists(account_data_dir):
        return {"data": {'account': account}, "historical": {}}  # data, clean

    data_range = filter_range(set_range, set_length)
    data_list = get_account_data_list(account_data_dir)
    chosen_data = get_files_from_range(data_list, account_data_dir, data_range)

    follower_count = []
    collection = []
    clean = []

    # Get the earliest dates / times based on the set length.
    for data_date in chosen_data:
        data = utils.read_json(data_date)

        for key, value in data.items():
            try:
                time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                time = datetime.strptime(key, "%Y-%m-%d")

        # name = value["name"]
        post_value = int(value["stats"][post_key])
        followers_value = int(value["stats"][followers_key])

        start_time = go_back_time(time, set_range, set_length)
        time_difference = time - start_time

    # Get the the latest data.
    no_duplicates_list = []

    for data_date in chosen_data:
        data = utils.read_json(data_date)

        prev_data = 10
        prev_post = None

        for prev, prev_value in data.items():
            try:
                time = datetime.strptime(prev, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(prev, "%Y-%m-%d")

            if start_time <= time:

                date = prev
                past_name = prev_value["name"]
                past_post_value = int(prev_value["stats"][post_key])
                past_followers_value = int(prev_value["stats"][followers_key])  # nopep8

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
                prev_data = past_followers_value
                growth = 100 - percent

                if growth < 80:
                    if value_data not in no_duplicates_list:

                        no_duplicates_list.append(value_data)

                        # Append when posted a new post.
                        if past_post_value != prev_post and prev_post != None:
                            posted_at_followers_count = past_followers_value
                        else:
                            posted_at_followers_count = None

                        prev_post = past_post_value

                        clean.append({
                            'date': date,
                            'name': past_name,
                            'post': past_post_value,
                            'followers': past_followers_value,
                            'postedAt': posted_at_followers_count,
                            'profile_picture_url': prev_value["stats"].get('profile_picture_url')
                        })

    # Compare data between the from and the to.
    prev_time = collection[0]

    for t in prev_time:
        name = prev_time[t]["name"]
        past_post_value = int(prev_time[t]["stats"][post_key])
        past_followers_value = int(prev_time[t]["stats"][followers_key])

        try:
            t_date = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            t_date = datetime.strptime(t + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")  # nopep8

        post_difference = int(post_value) - int(past_post_value)
        followers_difference = int(followers_value) - int(past_followers_value)

        average_per_10_min = calculate_average_difference(follower_count)

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

            "average_per_10_min": average_per_10_min,
            "average_per_1_hour": round(average_per_10_min * 6, 2),
            "average_per_1_day": round(average_per_10_min * 24, 2),
            "average_per_1_week": round(average_per_10_min * (24 * 7), 2),
            "average_per_1_month": round(average_per_10_min * (24 * 30), 2),

            "platform": platform
        }

    return {
        "data": data,
        "historical": clean
    }


def get_keys(platform):
    """ Returns keys for specific platforms to be used when extracting data """

    post_key = ""
    followers_key = ""

    if platform == 'instagram':
        post_key = "post_value"
        followers_key = "followers_value"

    if platform == 'tiktok':
        post_key = "likes"
        followers_key = "followers_value"

    if platform == 'bluesky':
        post_key = "posts_count"
        followers_key = "followers_count"

    if platform == 'youtube':
        post_key = "video_count"
        followers_key = "subscriber_count"

    if platform == 'x-twitter':
        post_key = "tweets_value"
        followers_key = "followers_value"

    return post_key, followers_key


def get_account_data_list(account_path):
    """ Returns and sorts paths to all data from the accounts data directory """

    sorted_list = None
    if os.path.isdir(account_path):
        data_list = os.listdir(account_path)

        # Sort based on the integer part before the underscore
        sorted_list = sorted(data_list, key=lambda x: int(x.split('_')[0]))

    return sorted_list


def filter_range(range, interval):
    """ Returns all the data for specific month if exists. """

    search_from = ""
    search_to = current_datetime = datetime.now()

    if range == "minute":
        search_from = current_datetime - timedelta(minutes=interval)

    if range == "hour":
        search_from = current_datetime - timedelta(hours=interval)

    if range == "day":
        search_from = current_datetime - timedelta(days=interval)

    if range == "week":
        search_from = current_datetime - timedelta(weeks=interval)

    if range == "month":
        search_from = current_datetime - timedelta(days=interval)

    if range == "year":
        search_from = current_datetime - timedelta(days=interval)

    if range == "custom":
        print("TODO; if range == 'custom':")

    day_number = f"{search_from.day:02}"
    month_name = search_from.strftime("%B")
    year_number = search_from.strftime("%Y")

    data = {
        "month_name": month_name,
        "day_number": day_number,
        "year_number": year_number,
        "search_from": search_from,
        "search_to": search_to
    }

    return data


def go_back_time(time, range, interval):
    """ Return a date based on the range and interval """

    if range == "minute":
        f = time - timedelta(minutes=interval)

    if range == "hour":
        f = time - timedelta(hours=interval)

    if range == "day":
        f = time - timedelta(days=interval)

    if range == "week":
        f = time - timedelta(weeks=interval)

    if range == "month":
        f = time - timedelta(days=interval)

    if range == "year":
        f = time - timedelta(days=interval)

    if range == "custom":
        print("TODO; if range == 'custom':")

    return f


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


def maybe_append(date, range, interval):

    append_value = date

    try:
        datetime_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        datetime_object = datetime.strptime(
            date + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

    if range == "hours" and interval > 6:
        value = datetime_object.hour
        day = datetime_object.day
        append_value = str(day) + '_' + str(value)

    if range == "days":
        if interval > 1:
            day = datetime_object.day
            month = datetime_object.month
            append_value = str(month) + '_' + str(day)
        if interval == 1:
            value = datetime_object.hour
            day = datetime_object.day
            append_value = str(day) + '_' + str(value)

    return append_value


if __name__ == "__main__":

    interval = 1
    range = "hours"

    account = "time.in.progress"
    get_graph_data(account, range, interval, 'instagram')
