from datetime import datetime, date
from typing import Optional


class TimeUtils:
    DATE_FORMAT: str = "%Y-%m-%d"
    DATE_FORMAT_US: str = "%m/%d/%Y"
    TIME_FORMAT: str = "%H:%M:%S"
    TIME_FORMAT_WITHOUT_SEC: str = "%H:%M"
    DATE_TIME_FORMAT: str = "%Y-%m-%d-%H-%M-%S"
    DATE_TIME_FORMAT_UI: str  = "%Y/%m/%d %H:%M:%S"
    
    @staticmethod
    def get_epoch(
        datetime_obj: Optional[datetime] = None
    ) -> int:
        """
        Convert a given datetime object to epoch seconds.

        Args:
        - datetime_obj (datetime, optional): The datetime object to be converted.
          If not provided, the current datetime will be used.

        Returns:
        - int: The epoch seconds corresponding to the provided datetime object.

        Note:
        - If `datetime_obj` is not provided, the method uses the current datetime.
        """
        if not datetime_obj:
            datetime_obj = datetime.now()
        epoch_seconds = datetime.timestamp(datetime_obj) 
        return int(epoch_seconds) 

    @staticmethod
    def get_datetime_from_epoch(
        epoch_time: int,
        date_format: str = DATE_TIME_FORMAT
    ) -> str:
        if not epoch_time:
            raise ValueError("Please provide valid epoch time")
        return datetime.fromtimestamp(epoch_time).strftime(date_format)
        
    @staticmethod
    def get_time_of_day(
        hours: int, 
        minutes: int, 
        seconds: int, 
        date_time_obj: Optional[datetime] = None
    ) -> datetime:
        """
        Generate a datetime object with the provided hours, minutes, and seconds.

        Args:
        - hours (int): The hour value.
        - minutes (int): The minute value.
        - seconds (int): The second value.
        - date_time_obj (datetime, optional): The datetime object to modify.
          If not provided, the current datetime will be used.

        Returns:
        - datetime: The modified datetime object.

        Note:
        - If `date_time_obj` is not provided, the method uses the current datetime.
        """
        if not date_time_obj:
            date_time_obj = datetime.now()
        date_time_obj = date_time_obj.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
        return date_time_obj

    @staticmethod
    def get_time_of_today(
        hours: int, 
        minutes: int, 
        seconds: int
    ) -> datetime:
        """
        Generate a datetime object for today with the provided hours, minutes, and seconds.

        Args:
        - hours (int): The hour value.
        - minutes (int): The minute value.
        - seconds (int): The second value.

        Returns:
        - datetime: The datetime object for today with the specified time.
        """
        return TimeUtils.get_time_of_day(hours, minutes, seconds, datetime.now())

    @staticmethod
    def get_today_date() -> date: 
        return date.today()
    
    @staticmethod
    def get_today_date_str(
        time: bool = False
    ) -> str:
        """
        Get the date or date-time string for today.

        Args:
        - time (bool, optional): Flag to determine if the time should be included in the string.

        Returns:
        - str: The formatted date or date-time string for today.
        """
        if time:
            return TimeUtils.convert_to_date_time_str(datetime.now())
        else:
            return TimeUtils.convert_to_date_str(datetime.now())

    @staticmethod
    def convert_to_date_str(
        datetime_obj: datetime
    ) -> str:
        """
        Convert a datetime object to a date string.

        Args:
        - datetime_obj (datetime): The datetime object to convert.

        Returns:
        - str: The formatted date string.
        """
        return datetime_obj.strftime(TimeUtils.DATE_FORMAT)
    
    @staticmethod
    def convert_to_date_time_str(
        datetime_obj: datetime
    ) -> str:
        """
        Convert a datetime object to a date-time string.

        Args:
        - datetime_obj (datetime): The datetime object to convert.

        Returns:
        - str: The formatted date-time string.
        """
        return datetime_obj.strftime(TimeUtils.DATE_TIME_FORMAT)
    
    @staticmethod
    def combine_date_time(
        date: str,
        date_format: str,
        time: str,
        time_format: str
    ) -> datetime:
        if not date:
            raise ValueError("Please provide a valid date value")
        
        if not time:
            raise ValueError("Please provide a valid time value")
        
        date_temp = datetime.strptime(date, date_format)
        time_temp = datetime.strptime(time, time_format).time()
        
        # Merge date and time into a single datetime object
        datetime_obj = datetime.combine(date_temp, time_temp)
        return datetime_obj
    
    