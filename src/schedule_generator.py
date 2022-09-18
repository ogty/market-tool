from typing import List


class ScheduleGenerator:
    
    def __init__(
        self,
        hours: List[int],
        step: int = None,
        fill: bool = True,
        include: bool = True,
        delimiter: str = None
    ) -> None:
        self.step = 30 if step is None else step
        self.hours = hours
        self.fill = fill
        self.delimiter = ':' if delimiter is None else delimiter

        time_schedule = []
        for hour in hours:
            for minute in range(0, 60, self.step):
                if fill:
                    hour = str(hour).zfill(2)
                    minute = str(minute).zfill(2)

                time_schedule.append(f"{hour}{self.delimiter}{minute}")

        if include:
            if hours[-1] != 23:
                if fill:
                    time_schedule.append(f"{hours[-1] + 1}{self.delimiter}00")
                else:
                    time_schedule.append(f"{hours[-1] + 1}{self.delimiter}0")

        self.time_schedule = time_schedule

    def delete(
        self,
        del_schedules: List[str] = None,
        start: str = None,
        end: str = None
    ) -> List[str]:
        start = '' if start is None else start
        end = '' if end is None else end
        del_schedules = [] if del_schedules is None else del_schedules

        if not del_schedules:
            [self.time_schedule.remove(del_schedule) for del_schedule in del_schedules]

        if not start and not end:
            try:
                start_index = self.time_schedule.index(start)
                end_index = self.time_schedule.index(end)
                result = self.time_schedule[:start_index] + self.time_schedule[end_index:]
                return result
            except ValueError as error:
                print(f"Error: {error}")
        else:
            return self.time_schedule
    
    def addition(self, add_schedules: List[str]) -> List[str]:
        self.time_schedule += add_schedules
        self.reorder()
        return self.time_schedule

    def reorder(self) -> None:
        zero_twentyfour = {k: [] for k in range(25)}
        for ts in self.time_schedule:
            ts_splited = ts.split(f"{self.delimiter}")
            for hour in zero_twentyfour.keys():
                if int(ts_splited[0]) == hour:
                    zero_twentyfour[hour].append(int(ts_splited[1]))
                    zero_twentyfour[hour].sort()

        time_schedule = []
        for hour, minutes in zero_twentyfour.items():
            for minute in minutes:
                if self.fill:
                    hour = str(hour).zfill(2)
                    minute = str(minute).zfill(2)

                time_schedule.append(f"{hour}{self.delimiter}{minute}")

        self.time_schedule = time_schedule

    def __call__(self) -> List[str]:
        return self.time_schedule
