import time

import data_sources.kalshi_data as kdata
import data_sources.polymarket_data as pdata

k_start = time.time()
kalshi_markets = kdata.get_kalshi_markets()
k_end = time.time()
k_elapsed = k_end - k_start
print(f"Kalshi get markets time: {int(k_elapsed//60)} min {k_elapsed%60:.2f} sec")

p_start = time.time()
poly_markets = pdata.get_poly_markets()
p_end = time.time()
p_elapsed = p_end - p_start
print(f"Polymarket get markets time: {int(p_elapsed//60)} min {p_elapsed%60:.2f} sec")

print("Number of kalshi markets: ", len(kalshi_markets))
print("Number of polymarket markets: ", len(poly_markets))

# Kalshi get markets time: 13 min 41.26 sec
# Polymarket get markets time: 0 min 14.99 sec
# Number of kalshi markets:  20815
# Number of polymarket markets:  16791


# for i in range(4):
#     print(kalshi_markets[i]['title'])
#     print(kalshi_markets[i]['subtitle'])
#     print(kalshi_markets[i]['url'])