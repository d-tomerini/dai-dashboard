"""
Database Service
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dynaconf import Dynaconf
from scrape_and_visualize.config import settings


__username = settings.POSTGRES_USER
__password = settings.POSTGRES_PASSWORD
__host = settings.POSTGRES_HOST
__port = settings.POSTGRES_PORT
__user = f"{__username}:{quote_plus(__password)}"
__socket = f"{__host}:{__port}"
__sync_url = f"postgresql://{__user}@{__socket}"

engine = create_engine(__sync_url, echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(engine)
