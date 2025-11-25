from annoy import AnnoyIndex
import sqlite3
import pickle
import os
import numpy as np

# annoy (approx nearest neighbor oh yeah (?)) index which is useful for finding top-k nn
# https://github.com/spotify/annoy

DB_PATH = "db/markets.db"
INDEX_PATH = "db/kalshi_ann.ann"
ID_MAP_PATH = "db/id_map.pkl"

def load_vectors_from_db() -> list[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, vector FROM vectors")
    rows = cursor.fetchall()
    conn.close()

    vectors = []
    for ticker, blob in rows:
        vec = pickle.loads(blob)
        vectors.append((ticker, np.array(vec, dtype=float)))

    return vectors

def build_annoy_index() -> None:
    vectors = load_vectors_from_db()
    dim = len(vectors[0][1])
    index = AnnoyIndex(dim, 'angular')
    id_to_ticker = dict()

    for i, (ticker, vec) in enumerate(vectors):
        index.add_item(i, vec)
        id_to_ticker[i] = ticker

    index.build(100) # more trees is more precision but with performance tradeoff
    index.save(INDEX_PATH)

    with open(ID_MAP_PATH, "wb") as f:
        pickle.dump(id_to_ticker, f)

    