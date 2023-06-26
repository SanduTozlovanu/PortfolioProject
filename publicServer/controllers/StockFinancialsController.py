from exceptions import NotFoundException
from publicServer.DTOs.StockFinancesDto import StockFinancesDto
from publicServer.DTOs.StockRatiosDto import StockRatiosDto
from publicServer.Database.Models.Balance import Balance
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.FinancialStatement import FinancialStatement
from publicServer.Database.Models.KeyMetrics import KeyMetrics
from publicServer.Database.Models.Ratios import Ratios
from publicServer.Database.Models.Score import Score
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.session import db


class StockFinancialsController:
    @staticmethod
    def receive_financial_statement(company_name) -> FinancialStatement:
        company_financial_statement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_name).order_by(FinancialStatement.date.desc()).first()
        if company_financial_statement is None:
            raise NotFoundException("Company Financial Statement not found")
        return company_financial_statement

    @staticmethod
    def receive_company_finances(company_ticker) -> StockFinancesDto:
        company_balance: Balance = db.query(Balance).filter(
            Balance.ticker == company_ticker).first()
        if company_balance is None:
            raise NotFoundException("Company balance not found")

        company_ratios: Ratios = db.query(Ratios).filter(
            Ratios.ticker == company_ticker).first()
        if company_ratios is None:
            raise NotFoundException("Company ratios not found")

        company_key_metrics: KeyMetrics = db.query(KeyMetrics).filter(
            KeyMetrics.ticker == company_ticker).first()
        if company_key_metrics is None:
            raise NotFoundException("Company key metrics not found")

        company_score: Score = db.query(Score).filter(
            Score.ticker == company_ticker).first()
        if company_score is None:
            raise NotFoundException("Company score not found")

        company_statement: FinancialStatement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).order_by(FinancialStatement.date.desc()).first()
        if company_statement is None:
            raise NotFoundException("Company financial statement")
        return StockFinancesDto(balance=company_balance, ratios=company_ratios, score=company_score,
                                key_metrics=company_key_metrics, statement=company_statement)

    @staticmethod
    def receive_companies_ratios() -> list[StockRatiosDto]:
        stock_ratios_dtos: list[StockRatiosDto] = []
        snp_list: list[Company] = db.query(Company).filter(Company.sector != "Energy").all()
        for company in snp_list:
            company_ratios: Ratios = db.query(Ratios).filter(
                Ratios.ticker == company.ticker).first()
            if company_ratios is None:
                continue

            company_key_metrics: KeyMetrics = db.query(KeyMetrics).filter(
                KeyMetrics.ticker == company.ticker).first()
            if company_key_metrics is None:
                continue

            stockPrice: StockPrice = db.query(StockPrice).filter(
                StockPrice.ticker == company.ticker).first()
            if stockPrice is None:
                continue

            stock_ratios_dtos.append(
                StockRatiosDto(ratios=company_ratios, key_metrics=company_key_metrics, price=stockPrice.price))
        return stock_ratios_dtos
