from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

def fetch_data(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        return {"error": f"No data found for {symbol}"}

    current_price = data["Close"].iloc[-1]
    volume = int(data["Volume"].iloc[-1])
    prev_close = ticker.info.get("previousClose", None)

    percent_change = None
    if prev_close:
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)

    return {
        "symbol": symbol,
        "price": float(current_price),
        "volume": volume,
        "previous_close": prev_close,
        "percent_change": percent_change
    }

@app.get("/")
def read_root():
    return {"message": "Market Data API is running"}

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    return fetch_data(symbol)

# Index endpoints
@app.get("/nifty")
def get_nifty():
    return fetch_data("^NSEI")

@app.get("/banknifty")
def get_banknifty():
    return fetch_data("^NSEBANK")

@app.get("/sensex")
def get_sensex():
    return fetch_data("^BSESN")

@app.get("/nasdaq")
def get_nasdaq():
    return fetch_data("^IXIC")

@app.get("/dowjones")
def get_dowjones():
    return fetch_data("^DJI")

@app.get("/sp500")
def get_sp500():
    return fetch_data("^GSPC")
