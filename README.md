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

#### Setup ngrok for public URL in webhook
Install ngrok
```
brew install ngrok
```

Log in ngrok account and get the token
```
ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
```

Run ngrok in port 80
```
ngrok http 80
```

Copy the URL + /webhook to TradingView webhook
```
Forwarding   https://randomstring.ngrok.io -> http://localhost:80
```