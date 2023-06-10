from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from publicServer.Database.Models.Balance import Balance
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.CompanyProfile import CompanyProfile
from publicServer.Database.Models.FinancialStatement import FinancialStatement
from publicServer.Database.Models.KeyMetrics import KeyMetrics
from publicServer.Database.Models.LatestNew import LatestNew
from publicServer.Database.Models.PricePrediction import PricePrediction
from publicServer.Database.Models.Ratios import Ratios
from publicServer.Database.Models.Score import Score
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.base import Base

engine = create_engine(r"sqlite:///D:\Sandu\Sandu\PortfolioProject\publicServer\Database\companies.db",
                       echo=True, connect_args={'check_same_thread': False})
table_objects = [LatestNew.__table__, Company.__table__, CompanyProfile.__table__, Ratios.__table__,
                 FinancialStatement.__table__, StockPrice.__table__, Balance.__table__, KeyMetrics.__table__,
                 Score.__table__, PricePrediction.__table__]
Base.metadata.create_all(bind=engine, tables=table_objects)
Session = sessionmaker(bind=engine)
db = Session()
