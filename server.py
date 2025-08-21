# server.py
from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

# Define indices
INDICES = {
    "^NSEI": "NIFTY 50",
    "^NSEBANK": "BANK NIFTY",
    "^BSESN": "SENSEX",
    "NIFTY_MID_SELECT.NS": "MIDCAP SELECT",
    "^CNXSC": "SMALLCAP INDEX",
}

@app.get("/")
def home():
    return {"message": "Indian Market Index API is running 🚀"}

@app.get("/indices")
def get_indices():
    data = {}
    for symbol, name in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d", interval="1m").tail(1)["Close"].values[0]
            data[name] = round(float(price), 2)
        except Exception as e:
            data[name] = f"Error: {e}"
    return data
