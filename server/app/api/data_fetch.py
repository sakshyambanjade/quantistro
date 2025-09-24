from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services import data_ingestion, lstm_forecasting
from app.services.forecasting import simple_ma_forecast
import pandas as pd
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.get("/stock/raw")
async def get_stock_raw(symbol: str, period: str = "6mo"):
    if not symbol:
        raise HTTPException(status_code=400, detail="Query param 'symbol' is required")
    data = data_ingestion.fetch_stock_data(symbol, period=period)
    return {
        "status": "success" if data.get("prices") else "error",
        "symbol": symbol,
        "count": len(data.get("prices", [])),
        "error": data.get("error"),
        "sample": data.get("prices", [])[:5],
    }


@router.get("/stock/lstm-forecast")
async def get_stock_lstm_forecast(symbol: str, forecast_steps: int = 5, mode: str = "simple", period: str = "6mo"):
    try:
        if not symbol:
            raise HTTPException(status_code=400, detail="Query param 'symbol' is required")
        if forecast_steps <= 0:
            raise HTTPException(status_code=400, detail="'forecast_steps' must be > 0")

        # Fetch stock data
        data = data_ingestion.fetch_stock_data(symbol, period=period)

        # Handle errors from data_ingestion
        if not data or not data.get("prices"):
            raise HTTPException(
                status_code=422,
                detail=data.get("error", f"No data fetched for {symbol}")
            )

        df = pd.DataFrame(data["prices"])
        if df.empty or "close" not in df.columns:
            raise HTTPException(status_code=422, detail="No price data available for the given symbol")

        # Choose forecast mode
        if mode == "lstm":
            forecasted_values = lstm_forecasting.lstm_forecast(df, "close", forecast_steps=forecast_steps)
        elif mode == "simple":
            forecasted_values = simple_ma_forecast(df, "close", periods=forecast_steps)
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'simple' or 'lstm'")

        return {
            "status": "success",
            "symbol": symbol,
            "forecast": forecasted_values,
            "mode": mode,
            "period": period,
        }

    except HTTPException:
        raise
    except Exception as e:
        # Log detailed traceback for debugging
        logger.error("Error in lstm_forecast endpoint", exc_info=True)
        return JSONResponse(status_code=500, content={
            "status": "error",
            "detail": f"LSTM forecast failed: {str(e)}"
        })

