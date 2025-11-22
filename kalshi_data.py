import requests

def get_markets() -> list:
    series_url = "https://api.elections.kalshi.com/trade-api/v2/series"
    series = requests.get(series_url).json()["series"]
    valid_markets = []
    num_series = len(series)
    for i in range(num_series - 10, num_series): # only looking at a few series for now
        ticker = series[i]['ticker']
        markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={ticker}&status=open"
        markets = requests.get(markets_url).json()["markets"]
        for m in markets:
            if m:
                valid_markets.append(m)

    return valid_markets

def get_titles() -> list:
    markets = get_markets()
    titles = []
    num_markets = len(markets)
    for i in range(num_markets):
        titles.append(markets[i]['title'])
    
    return titles

markets = get_markets()
titles = get_titles()
print(titles[:10])

print(len(titles))