from datetime import datetime


class RevenueChartBarDto:
    def __init__(self, quarter: datetime, revenue: int):
        self.quarter = quarter.strftime("%Y-%m-%d")
        self.MillionsRevenue = int(revenue/1000000)
        self.revenueColor = "hsl(120, 70%, 70%)"
