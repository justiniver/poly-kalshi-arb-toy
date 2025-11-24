from sentence_transformers import SentenceTransformer, util
import json
import data_sources.kalshi_data as kdata
import data_sources.polymarket_data as pdata

kalshi_markets = kdata.get_markets()
poly_markets = pdata.get_markets()

def vectorize_kalshi(markets: list) -> list:
    with open("vectors/kalshi_embeddings.json") as f:
        kalshi_embeddings = json.load(f)
    for m in markets:
        ticker = m['ticker']
        vec = None
        if ticker in kalshi_embeddings:
            vec = kalshi_embeddings['ticker']
        else:
            a