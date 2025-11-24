from sentence_transformers import SentenceTransformer
import data_sources.kalshi_data as kdata
import data_sources.polymarket_data as pdata
import sqlite3
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

def init_db() -> None:
    conn = sqlite3.connect("db/markets.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vectors (
            ticker TEXT PRIMARY KEY,
            market_text TEXT,
            vector BLOB
        )
    """)
    conn.commit()
    conn.close()

def _ticker_exists(ticker: str) -> bool:
    conn = sqlite3.connect("db/markets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM vectors WHERE ticker = ?", (ticker,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def _insert_embedding(ticker, text, vector) -> None:
    conn = sqlite3.connect("db/markets.db")
    cursor = conn.cursor()
    blob = pickle.dumps(vector)
    cursor.execute("""
        INSERT OR REPLACE INTO vectors (ticker, market_text, vector)
        VALUES (?, ?, ?)
    """, (ticker, text, blob))
    conn.commit()
    conn.close()

# Create embeddings for all markets; probably only do this for kalshi
def vectorize(markets) -> None:
    init_db()
    for m in markets:
        ticker = m["ticker"]
        if _ticker_exists(ticker):
            continue
        text = m["custom_desc"]
        vec = model.encode(text)
        _insert_embedding(ticker, text, vec)

def create_kalshi_embeddings() -> None:
    kalshi_markets = kdata.get_markets()
    init_db()
    vectorize(kalshi_markets)