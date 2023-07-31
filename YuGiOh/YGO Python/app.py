import time

from flask_cors import CORS
from flask import Flask, jsonify
import sqlite3, logging

from sqlite3 import dbapi2 as sqlite

import API_Call
import config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_cards_by_query():
    start_time = time.time()

    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM Cards")
    cards = cursor.fetchall()

    cards = [{"id": card_id, "name": card_name} for card_id, card_name in cards]
    logging.info(f'Time to execute query: {time.time() - start_time}')

    return jsonify(cards)


@app.route('/<int:card_id>', methods=['GET'])
def get_card_by_id(card_id):
    start_time = time.time()

    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT * FROM Cards WHERE id = ?", (card_id,))
    card = cursor.fetchone()
    card = dict(card)
    print(card)

    logging.info(f'Time to execute query: {time.time() - start_time}')

    return jsonify(card)


if __name__ == '__main__':
    app.run(debug=True)
