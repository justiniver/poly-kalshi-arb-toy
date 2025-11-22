import requests

def get_all_contracts():
    series_url = "https://api.elections.kalshi.com/trade-api/v2/series"
    series = requests.get(series_url).json()["series"]
# markets_url = f"https://api.elections.kalshi.com/trade-api/v2/series/{ticker}/markets"
# markets = requests.get(markets_url).json()["markets"]


print(series[1]['ticker'])
