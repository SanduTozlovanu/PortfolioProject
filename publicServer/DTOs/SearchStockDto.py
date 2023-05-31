class SearchStockDto:
    def __init__(self, id: int, name: str, ticker: str, marketCap: int, beta: float, price: float, sector: str):
        self.id = id
        self.ticker = ticker
        self.name = name
        self.marketCap = SearchStockDto.number_to_string(marketCap)
        self.beta = beta
        self.price = price
        self.sector = sector

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

