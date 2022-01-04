# TODO: Make the interval selectable

def generate_schedule(hour_list, waste_schedule=[]) -> list:
    time_schedule = []

    for hour in hour_list:
        for minute in range(0, 51, 10):
            if len(str(hour)) == 1:
                hour = f"0{hour}"
            if len(str(minute)) == 1:
                minute = f"0{minute}"

            time_schedule.append(f"{hour}:{minute}")

    for waste in waste_schedule:
        time_schedule.remove(waste)

    return time_schedule