class PieChartDto:
    def __init__(self, label: str, value):
        self.id = label
        self.label = label
        self.value = round(value, 2)
