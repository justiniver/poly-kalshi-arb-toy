import requests

# https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide

BASE = "https://gamma-api.polymarket.com"

# only can get 500 markets at a time
def get_page_poly_markets(limit=500, offset=0) -> list:
    params = {
        "closed": "false",
        "limit": limit,
        "offset": offset,
    }
    page = requests.get(f"{BASE}/markets", params=params).json()
    for m in page:
        slug = m['slug']
        m['url'] = f"https://polymarket.com/market/{slug}"

    return page

def get_poly_markets() -> list:
    markets = []
    curr_offset = 0
    while True:
        page = get_page_poly_markets(offset=curr_offset)
        if not page:
            break
        markets.extend(page)
        limit = 500
        curr_offset += limit

    return markets