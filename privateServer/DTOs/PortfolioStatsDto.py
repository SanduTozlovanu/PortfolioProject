import math


class PortfolioStatsDto:
    def __init__(self, initialValue: float, currentValue: float, holdings: int, highestValue: float, lowestValue: float,
                 beta: float, portfolioReturn: float, snpReturn: float, chartData):
        self.initialValue = str(float(round(initialValue, 2))) + "$"
        self.currentValue = str(float(round(currentValue, 2))) + "$"
        self.holdings = int(round(holdings, 2))
        self.highestValue = str(float(round(highestValue, 2))) + "$"
        self.lowestValue = str(float(round(lowestValue, 2))) + "$"
        if math.isnan(beta):
            beta = 0.00
        self.beta = float(round(beta, 2))
        self.portfolioReturn = str(float(round(portfolioReturn, 2))) + "%"
        self.snpReturn = str(float(round(snpReturn, 2))) + "%"
        self.benchmarkDelta = str(float(round(portfolioReturn - snpReturn, 2))) + "%"
        self.chartData = chartData

