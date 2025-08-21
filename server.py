# server.py
from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

# ✅ Correct Yahoo Finance symbols mapping
INDICES = {
    '^NSEBANK': 'BANK NIFTY',
    '^NSEI': 'NIFTY 50',
    '^BSESN': 'SENSEX',
    'NIFTY_MID_SELECT.NS': 'MIDCAP SELECT',
    '^CNXSC': 'SMALLCAP INDEX'
}

def fetch_live_data():
    results = {}
    for symbol, name in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.history(period="1d", interval="1m")

            if not info.empty:
                latest = info.iloc[-1]
                prev_close = ticker.info.get("previousClose", None)

                price = round(float(latest["Close"]), 2)
                volume = int(latest["Volume"])
                change_pct = None

                if prev_close:
                    change_pct = round(((price - prev_close) / prev_close) * 100, 2)

                results[name] = {
                    "symbol": symbol,
                    "price": price,
                    "volume": volume,
                    "percent_change": change_pct
                }
            else:
                results[name] = {
                    "symbol": symbol,
                    "price": None,
                    "volume": None,
                    "percent_change": None
                }
        except Exception as e:
            results[name] = {"error": str(e)}
    return results

@app.get("/")
def read_root():
    return {"message": "Welcome to Market Data API. Use /indices to fetch data."}

@app.get("/indices")
def get_indices():
    return fetch_live_data()
