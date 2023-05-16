from publicServer.DataCollector.Database.Models.Balance import Balance
from publicServer.DataCollector.Database.Models.FinancialStatement import FinancialStatement
from publicServer.DataCollector.Database.Models.KeyMetrics import KeyMetrics
from publicServer.DataCollector.Database.Models.Ratios import Ratios
from publicServer.DataCollector.Database.Models.Score import Score


class StockFinancesDto:
    def __init__(self, score: Score, key_metrics: KeyMetrics, ratios: Ratios, balance: Balance,
                 statement: FinancialStatement):
        self.pe = round(key_metrics.peRatio, 2)
        self.priceToSales = round(key_metrics.priceToSalesRatio, 2)
        self.ebtPerEbit = round(ratios.ebtPerEbit, 2)
        self.freeCashFlowYield = str(round(key_metrics.freeCashFlowYield * 100, 2)) + "%"
        self.evToEbitda = round(key_metrics.enterpriseValueOverEBITDA, 2)
        self.piotroskiScore = score.piotroskiScore
        self.altmanZScore = round(score.altmanZScore, 2)
        self.profitMargin = str(round(ratios.netProfitMargin * 100, 2)) + "%"
        self.operatingMargin = str(round(ratios.operatingProfitMargin * 100, 2)) + "%"
        self.totalInvestments = "$" + self.number_to_string(balance.totalInvestments)
        self.totalDebt = "$" + self.number_to_string(balance.totalDebt)
        self.totalCash = "$" + self.number_to_string(balance.totalCash)
        self.net = "$" + self.number_to_string(balance.totalCash - balance.totalDebt)
        self.revenue = "$" + self.number_to_string(statement.revenue)
        self.grossProfit = "$" + self.number_to_string(statement.grossProfit)
        self.netIncome = "$" + self.number_to_string(statement.netIncome)
        self.operatingExpenses = "$" + self.number_to_string(statement.operatingExpenses)
        self.priceToBookRatio = round(ratios.priceToBookRatio, 2)
        self.title = statement.title


    @staticmethod
    def number_to_string(number):
        suffixes = ["", "Th", "Ml", "Bl", "Tr", "Qd", "Qt"]

        if number == 0:
            return "Zero"

        # Calculate the magnitude of the number
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0

        # Format the number with the appropriate suffix
        formatted_number = "{:.2f}".format(number).rstrip("0").rstrip(".")
        return f"{formatted_number} {suffixes[magnitude]}"
