import axios from "axios";

const API_URL = "/api";

export async function getStockRaw(symbol) {
  const response = await axios.get(`${API_URL}/data/stock/raw`, {
    params: { symbol },
  });
  return response.data;
}

export async function getLstmForecast(symbol, steps) {
  const response = await axios.get(`${API_URL}/data/stock/lstm-forecast`, {
    params: { symbol, forecast_steps: steps },
  });
  return response.data;
}
