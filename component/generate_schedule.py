def generate_schedule(hour_list: list, step=30, include=True, fill=True, delimiter=":", addition=[], delete=[]) -> list:
    time_schedule = []
    for hour in hour_list:
        for minute in range(0, 60, step):
            if fill:
                hour = str(hour).zfill(2)
                minute = str(minute).zfill(2)

            time_schedule.append(f"{hour}{delimiter}{minute}")

    if include:
        if hour_list[-1] == 23:
            pass
        else:
            if fill:
                time_schedule.append(f"{hour_list[-1] + 1}:00")
            else:
                time_schedule.append(f"{hour_list[-1] + 1}:0")

    # Add and Sort
    for add_schedule in addition:
        time_schedule.append(add_schedule)

    one_twentyfour = {k: [] for k in range(25)}
    for ts in time_schedule:
        ts_splited = ts.split(":")
        for hour in one_twentyfour.keys():
            if int(ts_splited[0]) == hour:
                one_twentyfour[hour].append(int(ts_splited[1]))
                one_twentyfour[hour].sort()

    time_schedule = []
    for hour, minutes in one_twentyfour.items():
        for minute in minutes:
            if fill:
                hour = str(hour).zfill(2)
                minute = str(minute).zfill(2)

            time_schedule.append(f"{hour}:{minute}")

    # Delete schedule
    for del_schedule in delete:
        time_schedule.remove(del_schedule)

    return time_schedule