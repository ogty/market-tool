class ScheduleGenerator:
    def __init__(self, hours: list, step: int=30, fill: bool=True, include: bool=True, delimiter: str=":"):
        self.hours = hours
        self.fill = fill
        self.delimiter = delimiter

        time_schedule = []
        for hour in hours:
            for minute in range(0, 60, step):
                if fill:
                    hour = str(hour).zfill(2)
                    minute = str(minute).zfill(2)

                time_schedule.append(f"{hour}{delimiter}{minute}")

        if include:
            if hours[-1] == 23:
                pass
            else:
                if fill:
                    time_schedule.append(f"{hours[-1] + 1}{delimiter}00")
                else:
                    time_schedule.append(f"{hours[-1] + 1}{delimiter}0")

        self.time_schedule = time_schedule

    def delete(self, del_schedules: list=[], start: str="", end: str="") -> list:
        [self.time_schedule.remove(del_schedule) for del_schedule in del_schedules]

        if start != "" and end != "":
            try:
                start_index = self.time_schedule.index(start)
                end_index = self.time_schedule.index(end)
                result = self.time_schedule[:start_index] + self.time_schedule[end_index:]
                return result
            except ValueError as ex:
                print(f"Error: {ex}")
        else:
            return self.time_schedule
    
    def addition(self, add_schedule: list) -> list:
        self.time_schedule += add_schedule
        self.reorder()
        return self.time_schedule

    def reorder(self) -> None:
        one_twentyfour = {k: [] for k in range(25)}
        for ts in self.time_schedule:
            ts_splited = ts.split(f"{self.delimiter}")
            for hour in one_twentyfour.keys():
                if int(ts_splited[0]) == hour:
                    one_twentyfour[hour].append(int(ts_splited[1]))
                    one_twentyfour[hour].sort()

        time_schedule = []
        for hour, minutes in one_twentyfour.items():
            for minute in minutes:
                if self.fill:
                    hour = str(hour).zfill(2)
                    minute = str(minute).zfill(2)

                time_schedule.append(f"{hour}{self.delimiter}{minute}")

        self.time_schedule = time_schedule

    def __call__(self) -> list:
        return self.time_schedule