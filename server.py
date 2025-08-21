# server.py
from fastapi import FastAPI, Query
import yfinance as yf

app = FastAPI()

# Configure indices here (you can add/remove as needed)
INDICES = {
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "SENSEX": "^BSESN"
}

@app.get("/")
def home():
    return {"message": "Market Data API is running 🚀"}

@app.get("/price")
def get_price(symbol: str = Query(..., description="Yahoo Finance symbol e.g. ^NSEI")):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="1m")

    if hist.empty:
        return {"error": f"No data found for {symbol}"}

    latest = hist.iloc[-1]
    prev_close = ticker.history(period="2d").iloc[0]["Close"]
    change_percent = ((latest["Close"] - prev_close) / prev_close) * 100

    return {
        "symbol": symbol,
        "price": float(latest["Close"]),
        "volume": int(latest["Volume"]),
        "change_percent": round(change_percent, 2)
    }

@app.get("/indices")
def get_all_indices():
    results = {}
    for name, symbol in INDICES.items():
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1m")

        if hist.empty:
            results[name] = {"error": f"No data for {symbol}"}
            continue

        latest = hist.iloc[-1]
        prev_close = ticker.history(period="2d").iloc[0]["Close"]
        change_percent = ((latest["Close"] - prev_close) / prev_close) * 100

        results[name] = {
            "symbol": symbol,
            "price": float(latest["Close"]),
            "volume": int(latest["Volume"]),
            "change_percent": round(change_percent, 2)
        }
    return results
