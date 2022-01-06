def generate_schedule(hour_list: list, step=30, include=True, addition=[], delete=[]) -> list:
    time_schedule = []

    for hour in hour_list:
        for minute in range(0, 60, step):
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
    
    for add_schedule in addition:
        time_schedule.append(add_schedule)

    for del_schedule in delete:
        time_schedule.remove(del_schedule)

    return time_schedule

if __name__ == "__main__":
    result = generate_schedule(range(9, 15), step=30, addition=["09:05"])
    print(result)