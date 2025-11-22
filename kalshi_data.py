import requests

# basically copied this - https://docs.kalshi.com/getting_started/quick_start_market_data

def get_kalshi_markets() -> list:
    series_url = "https://api.elections.kalshi.com/trade-api/v2/series"
    series = requests.get(series_url).json()["series"]
    valid_markets = []
    num_series = len(series)
    for i in range(num_series):
        ticker = series[i]['ticker']
        markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={ticker}&status=open"
        markets = requests.get(markets_url).json()["markets"]
        for m in markets:
            if m:
                m['url'] = f"https://kalshi.com/markets/{ticker}" # adding url entry in dict because it seems useful
                valid_markets.append(m)

    return valid_markets

# probably not necessary; just stick to calling get_kalshi_markets
def get_kalshi_titles() -> list:
    markets = get_kalshi_markets()
    titles = []
    num_markets = len(markets)
    for i in range(num_markets):
        titles.append(markets[i]['title'])
    
    return titles
