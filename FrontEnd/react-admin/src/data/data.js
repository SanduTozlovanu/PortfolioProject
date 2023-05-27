export const stockScreenerFilters = {
  "marketCap":[["Any", ""],
    ["Mega (400bln and more)", "marketCapMoreThan=400000000000"],
    ["Large (100bln to 400bln)", "marketCapMoreThan=100000000000&marketCapLowerThan=400000000000"],
    ["Mid (50bln to 100bln)", "marketCapMoreThan=50000000000&marketCapLowerThan=100000000000"],
    ["Small (up to 50bln)", "marketCapLowerThan=50000000000"]],

  "price":[["Any", ""],
    ["Over 100$", "priceMoreThan=100"],
    ["Over 50$", "priceMoreThan=50"],
    ["Over 20$", "priceMoreThan=20"],
    ["50$ to 100$", "priceMoreThan=50&priceLowerThan=100"],
    ["20$ to 50$", "priceMoreThan=20&priceLowerThan=50"],
    ["10$ to 20$", "priceMoreThan=10&priceLowerThan=20"],
    ["5$ to 10$", "priceMoreThan=5&priceLowerThan=10"],
    ["under 5$", "priceLowerThan=5"]],

  "beta":[["Any", ""],
    ["Under 0", "betaLowerThan=0"],
    ["0 to 0.5", "betaLowerThan=0.5&betaMoreThan=0"],
    ["0.5 to 1", "betaLowerThan=1&betaMoreThan=0.5"],
    ["1 to 1.5", "betaLowerThan=1.5&betaMoreThan=1"],
    ["1.5 to 2", "betaLowerThan=2.5&betaMoreThan=1.5"],
    ["3 to 4", "betaLowerThan=4.5&betaMoreThan=3"],
    ["Over 4", "betaMoreThan=4"],
    ["under 5$", "betaLowerThan=5"]],

  "volume":[["Any", ""],
    ["Over 2M", "volumeMoreThan=2000000"],
    ["Over 1M", "volumeMoreThan=1000000"],
    ["Over 500K", "volumeMoreThan=500000"],
    ["500K to 1M", "volumeLowerThan=1000000&volumeMoreThan=500000"],
    ["100K to 500K", "volumeLowerThan=500000&volumeMoreThan=100000"],
    ["Under 700K", "volumeLowerThan=700000"],
    ["Under 500K", "volumeLowerThan=500000"],
    ["Under 200K", "volumeLowerThan=200000"],
    ["Under 100K", "volumeLowerThan=100000"],
    ["Under 50K", "volumeLowerThan=50000"]],

  "dividends":[["Any", ""],
    ["Over 10%", "dividendMoreThan=10"],
    ["Over 8%", "dividendMoreThan=8"],
    ["Over 6%", "dividendMoreThan=6"],
    ["Over 4%", "dividendMoreThan=4"],
    ["Over 2%", "dividendMoreThan=2"],
    ["0% to 1%", "dividendLowerThan=1"],
    ["0%", "dividendLowerThan=0"]],

  "sector":[["Any", ""],
    ["Basic Materials", "Basic Materials"],
    ["Communication Services", "Communication Services"],
    ["Consumer Cyclical", "Consumer Cyclical"],
    ["Consumer Defensive", "Consumer Defensive"],
    ["Energy", "Energy"],
    ["Financial", "Financial"],
    ["Industrials", "Industrials"],
    ["Real Estate", "Real Estate"],
    ["Technology", "Technology"],
    ["Utilities", "Utilities"],
    ["Industrial Goods", "Industrial Goods"],
    ["Services", "Services"],
    ["Conglomerates", "Conglomerates"],
    ["Financial Services", "Financial Services"]]
}