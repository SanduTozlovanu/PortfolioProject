from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataCollector.Database.base import Base

engine = create_engine("sqlite:///DataCollector/Database/companies.db", echo=True)
#table_objects = [LatestNew.__table__, Company.__table__, CompanyProfile.__table__]
Base.metadata.create_all(bind=engine, tables=Base.metadata.tables.values())
Session = sessionmaker(bind=engine)
db = Session()
