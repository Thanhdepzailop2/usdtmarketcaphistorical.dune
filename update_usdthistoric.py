import requests
import os
from datetime import datetime

# --- Config ---
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/tether"
DUNE_API = "https://api.dune.com/api/v1/table/upsert"

# Lấy token từ biến môi trường (GitHub Actions sẽ set)
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
DUNE_TABLE_NAME = "usdt_marketcap_eth"

def get_usdt_marketcap():
    """Lấy market cap USDT từ CoinGecko"""
    response = requests.get(COINGECKO_API)
    data = response.json()
    market_cap = data["market_data"]["market_cap"]["usd"]
    return market_cap

def push_to_dune(market_cap):
    """Push dữ liệu lên Dune table"""
    headers = {
        "x-dune-api-key": DUNE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "table_name": DUNE_TABLE_NAME,
        "data": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "market_cap_usd": market_cap
            }
        ]
    }
    response = requests.post(DUNE_API, headers=headers, json=payload)
    print("Push result:", response.status_code, response.text)

if __name__ == "__main__":
    mc = get_usdt_marketcap()
    print("USDT Market Cap (USD):", mc)
    push_to_dune(mc)
