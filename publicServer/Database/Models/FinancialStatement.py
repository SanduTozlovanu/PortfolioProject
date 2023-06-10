from datetime import datetime

from sqlalchemy import Column, String, Integer, BigInteger, Float, Date

from publicServer.Database.JsonAble import FinancialStatementJsonAble
from publicServer.Database.base import Base


class FinancialStatement(Base, FinancialStatementJsonAble):
    __tablename__ = "financialStatements"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    title = Column("title", String, nullable=False)
    date = Column("date", Date, nullable=False)
    period = Column("period", String, nullable=False)
    revenue = Column("revenue", BigInteger, nullable=False)
    costOfRevenue = Column("costOfRevenue", BigInteger, nullable=False)
    grossProfit = Column("grossProfit", BigInteger, nullable=False)
    grossProfitRatio = Column("grossProfitRatio", BigInteger, nullable=False)
    researchAndDevelopmentExpenses = Column("researchAndDevelopmentExpenses", BigInteger, nullable=False)
    generalAndAdministrativeExpenses = Column("generalAndAdministrativeExpenses", BigInteger, nullable=False)
    sellingAndMarketingExpenses = Column("sellingAndMarketingExpenses", BigInteger, nullable=False)
    sellingGeneralAndAdministrativeExpenses = Column("sellingGeneralAndAdministrativeExpenses", BigInteger, nullable=False)
    otherExpenses = Column("otherExpenses", BigInteger, nullable=False)
    operatingExpenses = Column("operatingExpenses", BigInteger, nullable=False)
    costAndExpenses = Column("costAndExpenses", BigInteger, nullable=False)
    interestIncome = Column("interestIncome", BigInteger, nullable=False)
    interestExpense = Column("interestExpense", BigInteger, nullable=False)
    depreciationAndAmortization = Column("depreciationAndAmortization", BigInteger, nullable=False)
    ebitda = Column("ebitda", BigInteger, nullable=False)
    ebitdaratio = Column("ebitdaratio", Float, nullable=False)
    operatingIncome = Column("operatingIncome", BigInteger, nullable=False)
    operatingIncomeRatio = Column("operatingIncomeRatio", Float, nullable=False)
    totalOtherIncomeExpensesNet = Column("totalOtherIncomeExpensesNet", BigInteger, nullable=False)
    incomeBeforeTax = Column("incomeBeforeTax", BigInteger, nullable=False)
    incomeTaxExpense = Column("incomeTaxExpense", BigInteger, nullable=False)
    incomeBeforeTaxRatio = Column("incomeBeforeTaxRatio", Float, nullable=False)
    netIncome = Column("netIncome", BigInteger, nullable=False)
    netIncomeRatio = Column("netIncomeRatio", Float, nullable=False)
    eps = Column("eps", Float, nullable=False)
    epsdiluted = Column("epsdiluted", Float, nullable=False)
    weightedAverageShsOut = Column("weightedAverageShsOut", BigInteger, nullable=False)
    weightedAverageShsOutDil = Column("weightedAverageShsOutDil", BigInteger, nullable=False)
    finalLink = Column("finalLink", String, nullable=False)

    def __init__(self, ticker, date: datetime, period, revenue, costOfRevenue, grossProfit, grossProfitRatio, researchAndDevelopmentExpenses,
                generalAndAdministrativeExpenses, sellingAndMarketingExpenses, sellingGeneralAndAdministrativeExpenses,
                otherExpenses, operatingExpenses, costAndExpenses, interestIncome, interestExpense,
                depreciationAndAmortization, ebitda, ebitdaratio, operatingIncome, operatingIncomeRatio,
                totalOtherIncomeExpensesNet, incomeBeforeTax, incomeTaxExpense, incomeBeforeTaxRatio, netIncome,
                netIncomeRatio, eps, epsdiluted, weightedAverageShsOut, weightedAverageShsOutDil, finalLink):
        self.ticker = ticker
        self.title = str(date.date()) + " " + period
        self.date = date
        self.period = period
        self.revenue = revenue
        self.costAndExpenses = costAndExpenses
        self.costOfRevenue = costOfRevenue
        self.grossProfit = grossProfit
        self.grossProfitRatio = grossProfitRatio
        if researchAndDevelopmentExpenses:
            self.researchAndDevelopmentExpenses = researchAndDevelopmentExpenses
        else:
            self.researchAndDevelopmentExpenses = 0
        if generalAndAdministrativeExpenses:
            self.generalAndAdministrativeExpenses = generalAndAdministrativeExpenses
        else:
            self.generalAndAdministrativeExpenses = 0
        if sellingAndMarketingExpenses:
            self.sellingAndMarketingExpenses = sellingAndMarketingExpenses
        else:
            self.sellingAndMarketingExpenses = 0
        if sellingGeneralAndAdministrativeExpenses:
            self.sellingGeneralAndAdministrativeExpenses = sellingGeneralAndAdministrativeExpenses
        else:
            self.sellingGeneralAndAdministrativeExpenses = 0
        if otherExpenses:
            self.otherExpenses = otherExpenses
        else:
            self.otherExpenses = 0
        if operatingExpenses:
            self.operatingExpenses = operatingExpenses
        else:
            self.operatingExpenses = 0
        if interestIncome:
            self.interestIncome = interestIncome
        else:
            self.interestIncome = 0
        if interestExpense:
            self.interestExpense = interestExpense
        else:
            self.interestExpense = 0
        if depreciationAndAmortization:
            self.depreciationAndAmortization = depreciationAndAmortization
        else:
            self.depreciationAndAmortization = 0
        if ebitda:
            self.ebitda = ebitda
        else:
            self.ebitda = 0
        if ebitdaratio:
            self.ebitdaratio = ebitdaratio
        else:
            self.ebitdaratio = 0
        if operatingIncome:
            self.operatingIncome = operatingIncome
        else:
            self.operatingIncome = 0
        if operatingIncomeRatio:
            self.operatingIncomeRatio = operatingIncomeRatio
        else:
            self.operatingIncomeRatio = 0
        if totalOtherIncomeExpensesNet:
            self.totalOtherIncomeExpensesNet = totalOtherIncomeExpensesNet
        else:
            self.totalOtherIncomeExpensesNet = 0
        if incomeBeforeTax:
            self.incomeBeforeTax = incomeBeforeTax
        else:
            self.incomeBeforeTax = 0
        if incomeTaxExpense:
            self.incomeTaxExpense = incomeTaxExpense
        else:
            self.incomeTaxExpense = 0
        if incomeBeforeTaxRatio:
            self.incomeBeforeTaxRatio = incomeBeforeTaxRatio
        else:
            self.incomeBeforeTaxRatio = 0
        if netIncome:
            self.netIncome = netIncome
        else:
            self.netIncome = 0
        if netIncomeRatio:
            self.netIncomeRatio = netIncomeRatio
        else:
            self.netIncomeRatio = 0
        if eps:
            self.eps = eps
        else:
            self.eps = 0
        if epsdiluted:
            self.epsdiluted = epsdiluted
        else:
            self.epsdiluted = 0
        if weightedAverageShsOut:
            self.weightedAverageShsOut = weightedAverageShsOut
        else:
            self.weightedAverageShsOut = 0
        if weightedAverageShsOutDil:
            self.weightedAverageShsOutDil = weightedAverageShsOutDil
        else:
            self.weightedAverageShsOutDil = 0
        if finalLink:
            self.finalLink = finalLink
        else:
            self.finalLink = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"



