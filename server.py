from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow all origins (so your Lovable app can fetch data)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Indices to fetch
INDICES = {
    '^NSEI': 'NIFTY 50',
    '^NSEBANK': 'BANK NIFTY',
    '^BSESN': 'SENSEX',
    'NIFTY_MID_SELECT.NS': 'MIDCAP SELECT',
    '^CNXSC': 'SMALLCAP INDEX'
}

@app.get("/indices")
def get_indices():
    result = {}
    for symbol, name in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            last_price = info.get("regularMarketPrice") or 0
            prev_close = info.get("regularMarketPreviousClose") or last_price
            change_percent = ((last_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
            volume = info.get("volume") or 0

            result[name] = {
                "symbol": symbol,
                "price": round(last_price, 2),
                "volume": volume,
                "percent_change": round(change_percent, 2)
            }

        except Exception as e:
            result[name] = {
                "symbol": symbol,
                "price": 0,
                "volume": 0,
                "percent_change": 0
            }
    return result


