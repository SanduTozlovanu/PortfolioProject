from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from publicServer.DataCollector.Database.Models.Balance import Balance
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.Database.Models.FinancialStatement import FinancialStatement
from publicServer.DataCollector.Database.Models.KeyMetrics import KeyMetrics
from publicServer.DataCollector.Database.Models.LatestNew import LatestNew
from publicServer.DataCollector.Database.Models.Ratios import Ratios
from publicServer.DataCollector.Database.Models.Score import Score
from publicServer.DataCollector.Database.Models.StockPrice import StockPrice
from publicServer.DataCollector.Database.base import Base

engine = create_engine(r"sqlite:///D:\Sandu\Sandu\PortfolioProject\publicServer\DataCollector\Database\companies.db", echo=True, connect_args={'check_same_thread': False})
table_objects = [LatestNew.__table__, Company.__table__, CompanyProfile.__table__, Ratios.__table__,
                 FinancialStatement.__table__, StockPrice.__table__, Balance.__table__, KeyMetrics.__table__,
                 Score.__table__]
Base.metadata.create_all(bind=engine, tables=table_objects)
Session = sessionmaker(bind=engine)
db = Session()
