def generate_schedule(hour_list: list, step=30, include=True, waste_schedule=[]) -> list:
    time_schedule = []

    for hour in hour_list:
        for minute in range(0, 51, step):
            if len(str(hour)) == 1:
                hour = f"0{hour}"
            if len(str(minute)) == 1:
                minute = f"0{minute}"

            time_schedule.append(f"{hour}:{minute}")

    if include:
        if hour_list[-1] == 23:
            pass
        else:
            time_schedule.append(f"{hour_list[-1] + 1}:00")
        
    for waste in waste_schedule:
        time_schedule.remove(waste)

    return time_schedule