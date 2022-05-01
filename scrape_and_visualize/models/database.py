"""
Define the models used in the database
"""

from scrape_and_visualize.services.database import Base
from sqlalchemy import Column, Integer, String, TIME


class DB_Runner(Base):
    """
    Defines how experiment data is structured in DB
    """

    __tablename__ = "runners"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Category = Column(String)
    Rang = Column(String)
    Fullname = Column(String)
    Age_year = Column(Integer)
    Location = Column(String)
    total_time = Column(TIME())
    run_link = Column(String)
    run_year = Column(Integer)
