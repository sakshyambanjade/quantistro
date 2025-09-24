import yfinance as yf
import logging

logger = logging.getLogger("uvicorn.error")

def fetch_stock_data(symbol: str, period: str = "6mo"):
    ticker = yf.Ticker(symbol)

    try:
        hist = ticker.history(period=period)
    except Exception as e:
        logger.warning(f"yfinance history() failed for symbol={symbol}: {e}")
        return {"symbol": symbol, "prices": [], "error": f"yfinance failed: {e}"}

    if hist is None or hist.empty:
        logger.warning(f"No historical data returned for symbol={symbol}")
        return {"symbol": symbol, "prices": [], "error": "No historical data"}

    # Convert to dict suitable for JSON response
    data = hist.reset_index()
    prices = []
    for _, row in data.iterrows():
        try:
            prices.append({
                "date": row["Date"].strftime("%Y-%m-%d"),
                "close": float(row["Close"]),
            })
        except Exception:
            continue

    if not prices:
        logger.warning(f"Parsed price list empty for symbol={symbol}")
        return {"symbol": symbol, "prices": [], "error": "No parsed prices"}

    return {"symbol": symbol, "prices": prices}
