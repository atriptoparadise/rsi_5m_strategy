# rsi_5m_strategy
Receive webhook from TradingView and process trade orders.

#### This endpoint expects a JSON payload with the following fields:
- side: The side of the trade, either "BUY" or "SELL".
- symbol: The trading symbol for the asset.
- close: The closing price of the asset.

#### message from TradingView
```json
{
  "side": "{{strategy.order.action}}",
  "symbol": "{{ticker}}",
  "close": "{{close}}"
}
```