from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.Database.Models.LatestNew import LatestNew
from publicServer.DataCollector.Database.base import Base

engine = create_engine(r"sqlite:///D:\Sandu\Sandu\PortfolioProject\publicServer\DataCollector\Database\companies.db", echo=True)
table_objects = [LatestNew.__table__, Company.__table__, CompanyProfile.__table__]
Base.metadata.create_all(bind=engine, tables=table_objects)
Session = sessionmaker(bind=engine)
db = Session()
