import requests
import json
from datetime import datetime
from config import ORDERS_URL, HEADERS

import logging
logfile = 'logs/signal_{}.log'.format(datetime.now().date())
logging.basicConfig(filename=logfile, level=logging.WARNING)

from flask import Flask, request, jsonify
app = Flask(__name__)


def create_order(symbol, qty, side, order_type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    logging.warning(json.loads(r.content))
    return json.loads(r.content)


@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive webhook from TradingView"""
    try:
        data = request.json  # Get JSON data
        logging.info(f"Received Webhook: {data}")

        response = {
            "status": "success",
            "received": data
        }
        print(response)
        return jsonify(response), 200
    
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

