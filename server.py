from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Market Data API is live 🎉"}

# Function to fetch live price
def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    if data.empty:
        return {"error": f"No data for {symbol}"}
    last_row = data.iloc[-1]
    return {
        "symbol": symbol,
        "price": float(last_row["Close"]),
        "volume": int(last_row["Volume"])
    }

# Nifty50 endpoint
@app.get("/nifty")
def nifty():
    return get_price("^NSEI")

# Bank Nifty endpoint
@app.get("/banknifty")
def banknifty():
    return get_price("^NSEBANK")

# Sensex endpoint
@app.get("/sensex")
def sensex():
    return get_price("^BSESN")

# Midcap endpoint
@app.get("/midcap")
def midcap():
    return get_price("^NSEMDCP50")

# Smallcap endpoint
@app.get("/smallcap")
def smallcap():
    return get_price("^NSESCAP")
