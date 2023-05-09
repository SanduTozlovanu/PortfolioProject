from abc import ABC


import requests
from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.FinancialStatement import FinancialStatement
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_MINUTE
from publicServer.config.definitions import KEY_URL


class GetFinancialStatements(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 5, 10)
        self.url = API_ENDPOINT + "v3/income-statement/{}?period=quarter&limit=" + str(self.rate_cost) + "&" + KEY_URL
        self.collectList = []

    def execute(self):
        for ticker in db.query(Company.ticker).all():
            ticker = ticker.ticker
            statement = db.query(FinancialStatement).filter(FinancialStatement.ticker == ticker).first()
            if not statement:
                self.collectList.append(ticker)
                if len(self.collectList) >= self.rate_cost:
                    break
        for i in range(0, len(self.collectList)):
            self.prepareRequest(i)
            result = requests.get(self.url)
            if result.status_code == 200:
                self.collectData(result.json())
            else:
                print(f"[GetFinancialStatements] failed to get company financial statement {result.status_code}")
                return

    def prepareRequest(self, index):
        self.url = API_ENDPOINT + "v3/income-statement/{}?period=quarter&limit=" + str(self.rate_cost) + "&" + KEY_URL
        self.url = self.url.format(self.collectList[index])

    @staticmethod
    def collectData(result):
        for statement in result:
            financial_statement = FinancialStatement(ticker=statement["symbol"], date=statement["date"], period=statement["period"],
                                                     revenue=statement["revenue"], costOfRevenue=statement["revenue"], grossProfit=statement["grossProfit"],
                                                     grossProfitRatio=statement["grossProfitRatio"], researchAndDevelopmentExpenses=statement["researchAndDevelopmentExpenses"],
                                                     generalAndAdministrativeExpenses=statement["generalAndAdministrativeExpenses"], sellingAndMarketingExpenses=statement["sellingAndMarketingExpenses"],
                                                     sellingGeneralAndAdministrativeExpenses=statement["sellingGeneralAndAdministrativeExpenses"],
                                                     otherExpenses=statement["otherExpenses"], operatingExpenses=statement["operatingExpenses"],
                                                     costAndExpenses=statement["costAndExpenses"], interestIncome=statement["interestIncome"],
                                                     interestExpense=statement["interestExpense"], depreciationAndAmortization=statement["depreciationAndAmortization"],
                                                     ebitda=statement["ebitda"], ebitdaratio=statement["ebitdaratio"], operatingIncome=statement["operatingIncome"],
                                                     operatingIncomeRatio=statement["operatingIncomeRatio"], totalOtherIncomeExpensesNet=statement["totalOtherIncomeExpensesNet"],
                                                     incomeBeforeTax=statement["incomeBeforeTax"], incomeTaxExpense=statement["incomeTaxExpense"],
                                                     incomeBeforeTaxRatio=statement["incomeBeforeTaxRatio"], netIncome=statement["netIncome"],
                                                     netIncomeRatio=statement["netIncomeRatio"], eps=statement["eps"], epsdiluted=statement["epsdiluted"],
                                                     weightedAverageShsOut=statement["weightedAverageShsOut"], weightedAverageShsOutDil=statement["weightedAverageShsOutDil"],
                                                     finalLink=statement["finalLink"])
            db.add(financial_statement)
        db.commit()
