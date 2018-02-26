from lollibot.config import config

from datetime import date, time, datetime


class Scheduler(object):

    def __init__(self):
        pass

    @staticmethod
    def __config_key(date: date) -> str:
        return "SCHEDULE_{}".format(date)

    def __parse_time(self, time_str: str) -> time:
        return datetime.strptime(time_str, "%H:%M:%S").time()

    def set_schedule(self, date: date, schedule: list) -> None:
        config.set(self.__config_key(date), schedule)

    def delete_schedule(self, date: date) -> None:
        # Cleaner than set_schedule(self, []), because cleans config
        config.set(self.__config_key(date), None)

    def get_schedule(self, date: date) -> list:
        return config.get(self.__config_key(date)) or []

    def in_schedule_dt(self, datetime: datetime) -> bool:
        return self.in_schedule(datetime.date(), datetime.time())

    def in_schedule(self, date: date, cur_time: time) -> bool:
        schedule = self.get_schedule(date)

        if schedule is None:
            return False

        for timeslot in schedule:
            sp = timeslot.split('-')
            start = self.__parse_time(sp[0])
            end = self.__parse_time(sp[1])
            if start <= cur_time <= end:
                return True

        return False
