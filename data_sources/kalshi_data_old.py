import requests

# basically copied this - https://docs.kalshi.com/getting_started/quick_start_market_data
series_url = "https://api.elections.kalshi.com/trade-api/v2/series"

# helper to generate custom desc string which we will vectorize
def _generate_custom_desc(m: dict) -> str:
    builder = []
    title = m['title']
    subtitle = m['subtitle']
    # category = m['category']
    rules = m['rules_primary']

    # I think some of these are guaranteed to be nonempty but doing this anyway
    if title:
        builder.append(f"Market title: {title}")
    if subtitle:
        builder.append(f"Subtitle: {subtitle}.")
    # if category:
    #     builder.append(f"Category: {category}.")
    if rules:
        builder.append(f"Rules: {rules}")

    return " ".join(builder)

def get_markets() -> list[dict]:
    series = requests.get(series_url).json()["series"]
    print(series)
    valid_markets = []
    num_series = len(series)
    for i in range(num_series):
        ticker = series[i]['ticker']
        markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={ticker}&status=open"
        markets = requests.get(markets_url).json()["markets"]
        for m in markets:
            if m:
                m['url'] = f"https://kalshi.com/markets/{ticker}" # adding url entry in dict because it seems useful
                m['custom_desc'] = _generate_custom_desc(m)
                valid_markets.append(m)

    return valid_markets

def get_one_market() -> dict:
    series = requests.get(series_url).json()["series"]
    print(series)
    num_series = len(series)
    for i in range(num_series):
        ticker = series[i]['ticker']
        markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={ticker}&status=open"
        markets = requests.get(markets_url).json()["markets"]
        for m in markets:
            if m:
                m['url'] = f"https://kalshi.com/markets/{ticker}"
                m['custom_desc'] = _generate_custom_desc(m)
                return m

def print_market_info() -> None:
    m = get_one_market()
    print('\n', m, '\n')
    print(m['title'])
    print(m['subtitle'])
    print(m['yes_sub_title'])
    print(m['no_sub_title'])
    # print(m['category'])
    print(m['rules_primary'])
    print(m['custom_desc'])

print_market_info()