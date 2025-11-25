import requests

# https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide
base = "https://gamma-api.polymarket.com"

def _generate_custom_desc(m: dict) -> str:
    builder = []
    title = m['question']
    rules = m['description']

    # I think some of these are guaranteed to be nonempty but doing this anyway
    if title:
        builder.append(f"Market title: {title}")
    if rules:
        builder.append(f"Description: {rules}")

    return " ".join(builder)

# only can get 500 markets at a time; helper function but may be useful
def get_page_markets(limit=500, offset=0) -> list[dict]:
    params = {
        "closed": "false",
        "limit": limit,
        "offset": offset,
    }
    page = requests.get(f"{base}/markets", params=params).json()
    for m in page:
        slug = m['slug']
        m['url'] = f"https://polymarket.com/market/{slug}"
        m['custom_desc'] = _generate_custom_desc(m)

    return page

def get_markets() -> list[dict]:
    markets = []
    curr_offset = 0
    limit = 500
    while True:
        page = get_page_markets(offset=curr_offset)
        if not page:
            break
        markets.extend(page)
        curr_offset += limit

    return markets

def get_one_market() -> dict:
    return get_page_markets(limit=1)[0]

def print_market_info() -> None:
    m = get_one_market()
    print(m, '\n')
    print(m['question'])
    print(m['description'])
    print(m['custom_desc'])
    return