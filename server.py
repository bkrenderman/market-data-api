from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow Lovable and Vercel domains to access the API
origins = [
    "https://preview--bloom-bar.lovable.app",
    "https://tradediary-lilac.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define your indices
INDICES = {
    '^NSEBANK': 'BANK NIFTY',
    '^NSEI': 'NIFTY 50',
    '^BSESN': 'SENSEX',
    'NIFTY_MID_SELECT.NS': 'MIDCAP SELECT',
    '^CNXSC': 'SMALLCAP INDEX'
}

def fetch_live_data():
    result = {}
    for symbol, name in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                last_row = data.iloc[-1]
                prev_close = last_row['Close']
                # Compute change and percent
                open_price = last_row['Open']
                percent_change = ((prev_close - open_price) / open_price) * 100 if open_price != 0 else 0
                result[name] = {
                    "symbol": symbol,
                    "price": round(prev_close, 2),
                    "volume": int(last_row['Volume']),
                    "percent_change": round(percent_change, 2)
                }
            else:
                result[name] = {
                    "symbol": symbol,
                    "price": 0,
                    "volume": 0,
                    "percent_change": 0
                }
        except Exception as e:
            result[name] = {
                "symbol": symbol,
                "price": 0,
                "volume": 0,
                "percent_change": 0
            }
    return result

@app.get("/indices")
def get_indices():
    return fetch_live_data()
