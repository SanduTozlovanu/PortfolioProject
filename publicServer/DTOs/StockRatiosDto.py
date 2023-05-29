from publicServer.DataCollector.Database.Models.KeyMetrics import KeyMetrics
from publicServer.DataCollector.Database.Models.Ratios import Ratios


class StockRatiosDto:
    def __init__(self, key_metrics: KeyMetrics, ratios: Ratios, price: float):
        self.ticker = key_metrics.ticker
        self.price = price
        self.peRatio = round(key_metrics.peRatio, 2)
        self.priceToSales = round(key_metrics.priceToSalesRatio, 2)
        self.ebtPerEbit = round(ratios.ebtPerEbit, 2)
        self.freeCashFlowYield = round(key_metrics.freeCashFlowYield * 100, 2)
        self.evToEbitda = round(key_metrics.enterpriseValueOverEBITDA, 2)
        self.profitMargin = round(ratios.netProfitMargin * 100, 2)
        self.operatingMargin = round(ratios.operatingProfitMargin * 100, 2)
        self.priceToBookRatio = round(ratios.priceToBookRatio, 2)
