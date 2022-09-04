from datetime import datetime, timedelta

from github_archive.conf.github_archive_conf import GithubArchiveConf
from github_archive.operators.bookmark import retrieve_last_file_name


def generate_file_name() -> list:
    file_list = list()
    initial_file = retrieve_last_file_name()
    extension = "." + ".".join(initial_file.split("/")[-1].split(".")[1:])
    initial_date_time = initial_file.split("/")[-1].split(".")[0]
    initial_date = datetime.strptime(
        "-".join(initial_date_time.split("-")[:-1]), "%Y-%m-%d"
    )
    initial_hour = initial_date_time.split("-")[-1]
    current_date = datetime.today()
    current_hour = datetime.strftime(datetime.now(), "%H")
    number_of_days = (current_date - initial_date).days
    day_counter = 0
    while day_counter <= number_of_days:
        if day_counter == 0 and number_of_days == 0:
            hour_start_counter = int(initial_hour) + 1
            hour_end_counter = int(current_hour)
        elif day_counter == 0 and number_of_days > 0:
            hour_start_counter = int(initial_hour) + 1
            hour_end_counter = 24
        elif day_counter == number_of_days:
            hour_start_counter = 0
            hour_end_counter = int(current_hour)
        else:
            hour_start_counter = 0
            hour_end_counter = 24
        file_list += [
            GithubArchiveConf.URL_PREFIX
            + datetime.strftime(initial_date + timedelta(days=day_counter), "%Y-%m-%d")
            + "-"
            + str(i)
            + extension
            for i in range(hour_start_counter, hour_end_counter)
        ]
        day_counter += 1
    return file_list


if __name__ == "__main__":
    print(generate_file_name())
