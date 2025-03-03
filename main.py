import requests
import json
from datetime import datetime
from config import ORDERS_URL, HEADERS, ACCOUNT_URL, POSITIONS_URL, AMOUNT

import logging
logfile = 'logs/signal_{}.log'.format(datetime.now().date())
logging.basicConfig(filename=logfile, level=logging.WARNING)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

from flask import Flask, request, jsonify
app = Flask(__name__)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    print("Account details:")
    print(json.loads(r.content))
    print("=====================================\n")


def create_order(symbol, qty, side, order_type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    logging.warning(f"{datetime.now()} - {json.loads(r.content)}")
    return json.loads(r.content)


def close_position(symbol):
    """Closes all positions for a given symbol"""
    url = f"{POSITIONS_URL}/{symbol}"
    response = requests.delete(url, headers=HEADERS)
    
    if response.status_code == 200:
        logging.warning(f"{datetime.now()} - Closed all positions for {symbol}")
        print(f"{datetime.now()} - Closed all positions for {symbol}")
        return {"status": "success", "message": f"Closed all positions for {symbol}"}
    else:
        logging.error(f"{datetime.now()} - Failed to close positions for {symbol}")
        print(f"{datetime.now()} - Failed to close positions for {symbol}")
        logging.error(response.json())
        return {"status": "error", "message": response.json()}


def get_position(symbol):
    """Checks if a position exists for a given symbol"""
    url = f"{POSITIONS_URL}/{symbol}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()  # Returns position details
    else:
        return None  # No position found
    

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive webhook from TradingView and process trade orders"""
    try:
        data = request.get_json()

        side = data.get("side")
        symbol = data.get("symbol")
        close = float(data.get("close"))

        if not all([side, symbol, close]):
            raise ValueError("Missing required fields in webhook payload.")

        if side.upper() == "SELL":
            # Close all positions for the symbol
            response = close_position(symbol)

        elif side.upper() == "BUY":
            # Check if we already hold this stock
            position = get_position(symbol)
            if position:
                response = {"status": "skipped", "message": f"Already holding {symbol}, skipping buy order."}
                print(f"{datetime.now()} - Already holding {symbol}, skipping buy order.")
                logging.warning(f"{datetime.now()} - Already holding {symbol}, skipping buy order.")
            else:
                qty = AMOUNT / close  # Calculate quantity to buy
                response = create_order(
                    symbol=symbol,
                    qty=qty,
                    side="buy",
                    order_type="market",
                    time_in_force="day"
                )
                print(f"{datetime.now()} - Buy order for {symbol} placed successfully.")
                logging.warning(f"{datetime.now()} - Buy order for {symbol} placed successfully.")

        else:
            response = {"status": "error", "message": "Invalid side provided."}

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    get_account()
    app.run(host='0.0.0.0', port=8888, debug=True)

