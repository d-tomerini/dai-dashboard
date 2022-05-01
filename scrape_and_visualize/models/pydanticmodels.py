from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class Runner(BaseModel):
    Fullname: str
    Category: str
    Rang: str
    Age_year: Optional[int]
    Location: str
    total_time: Optional[datetime]
    run_link: str
    run_year: int

    @validator('Age_year', pre=True)
    def year_is_null(cls, v):
        """
        This catches a particular null value on the database
        :param v: age_year to be saved as null
        :return:
        """
        if v == '????':
            return None
        return v

    @validator('total_time', pre=True)
    def parse_date(cls, t):
        """
        Parsed time from the runners website
        First catch is for invalid timestamps (disqualified runners)
        :return:
        """
        if "-" in t:
            return None
        try:
            timestamp = datetime.strptime(t, '%H:%M.%S,%f')
        except ValueError:
            timestamp = datetime.strptime(t, '%M.%S,%f')
        return timestamp
