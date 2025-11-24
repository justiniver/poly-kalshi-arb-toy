import requests

# https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide



# only can get 500 markets at a time
def get_page_markets(limit=500, offset=0) -> list:
    base = "https://gamma-api.polymarket.com"
    params = {
        "closed": "false",
        "limit": limit,
        "offset": offset,
    }
    page = requests.get(f"{base}/markets", params=params).json()
    for m in page:
        slug = m['slug']
        m['url'] = f"https://polymarket.com/market/{slug}"

    return page

def get_markets() -> list:
    markets = []
    curr_offset = 0
    while True:
        page = get_page_markets(offset=curr_offset)
        if not page:
            break
        markets.extend(page)
        limit = 500
        curr_offset += limit

    return markets

def get_one_market() -> dict:
    params = {
        "closed": "false",
        "limit": 1,
        "offset": 0,
    }
    market = requests.get(f"{BASE}/markets", params=params).json()
    slug = market[0]['slug']
    market[0]['url'] = f"https://polymarket.com/market/{slug}"

    return market[0]

def print_market_info() -> None:
    m = get_one_market()
    print(m, '\n')
    print(m['question'])
    print(m['description'])
    return

print_market_info()