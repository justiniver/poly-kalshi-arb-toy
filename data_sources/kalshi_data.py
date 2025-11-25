import requests

# basically copied this - https://docs.kalshi.com/getting_started/quick_start_market_data
# realized that pagination technique is way faster - https://docs.kalshi.com/api-reference/market/get-markets
base = "https://api.elections.kalshi.com/trade-api/v2"

# helper to generate custom desc string which we will vectorize
def _generate_custom_desc(m: dict) -> str:
    builder = []
    title = m['title']
    subtitle = m['subtitle']
    category = m['category']
    rules = m['rules_primary']

    # I think some of these are guaranteed to be nonempty but doing this anyway
    if title:
        builder.append(f"Market title: {title}")
    if subtitle:
        builder.append(f"Subtitle: {subtitle}.")
    if category:
        builder.append(f"Category: {category}.")
    if rules:
        builder.append(f"Rules: {rules}")

    return " ".join(builder)

def get_page_markets(limit=1000, cursor=None) -> tuple[list[dict], str]:
    params = {
        "status": "open",
        "limit": limit
    }

    if cursor:
        params["cursor"] = cursor

    data = requests.get(f"{base}/markets", params=params).json()
    page = data.get("markets")
    next_cursor = data.get("cursor")

    for m in page:
        ticker = m["ticker"]
        general_ticker = ticker.partition('-')[0]
        m['url'] = f"https://kalshi.com/markets/{general_ticker}"
        m['custom_desc'] = _generate_custom_desc(m)

    return (page, next_cursor)

def get_markets() -> list[dict]:
    markets = []
    cursor = None
    while True:
        page, cursor = get_page_markets(cursor=cursor)
        if not page:
            break
        markets.extend(page)
        if not cursor:
            break

    return markets

def get_one_market() -> dict:
    markets, _ = get_page_markets(limit=1)
    m = markets[0]
    return m

def print_market_info(m: dict) -> None:
    print(m, '\n')
    print(m['title'])
    print(m['subtitle'])
    print(m['yes_sub_title'])
    print(m['no_sub_title'])
    print(m['category'])
    print(m['rules_primary'])
    print(m['custom_desc'])
    print(m['url'])
    return