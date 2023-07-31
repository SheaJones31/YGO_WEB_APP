import datetime
import json
import sqlite3

import API_Request, data_verify, query_print, config

import logging
logging.basicConfig(level=logging.INFO)


def card_api_request(DATA_STORAGE_FILE):
    try:
        # Writes to response.txt file for updating information
        API_Request.main(DATA_STORAGE_FILE)
    except Exception as e:
        logging.info(f"Error loading API request {e}")


def card_data_request(DATA_STORAGE_FILE):
    with open(DATA_STORAGE_FILE, 'r') as f:
        response_text = f.read()
    return json.loads(response_text)


def create_card_table(cursor):

    cursor.execute("DROP TABLE IF EXISTS Cards")

    cursor.execute('''
            CREATE TABLE Cards
            (id INT PRIMARY KEY,
            name TEXT,
            type TEXT,
            frameType TEXT,
            desc TEXT,
            atk INT,
            def INT,
            level INT,
            race TEXT,
            attribute TEXT,
            archetype TEXT,
            image_url TEXT,
            image_small TEXT,
            image_cropped TEXT)
        ''')


def create_set_table(cursor):

    cursor.execute("DROP TABLE IF EXISTS Card_Set")

    cursor.execute('''
            CREATE TABLE Card_Set
            (id INT,
            set_name TEXT,
            set_code TEXT,
            set_rarity TEXT,
            set_rarity_code TEXT,
            set_price REAL,
            FOREIGN KEY (id) REFERENCES Cards (id))
        ''')


def create_price_table(cursor):

    cursor.execute("DROP TABLE IF EXISTS Card_Price")

    cursor.execute('''
            CREATE TABLE Card_Price
            (id INT,
            cardmarket_price REAL,
            tcgplayer_price REAL,
            ebay_price REAL,
            amazon_price REAL,
            coolstuffinc_price REAL,
            FOREIGN KEY (id) REFERENCES Cards (id))
        ''')


def insert_card_table(cursor, card_data):

    insert_query = "INSERT OR IGNORE INTO Cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    card_tuples = []
    for card in card_data['data']:
        card_tuple = (
            card['id'],
            card['name'],
            card['type'],
            card['frameType'],
            card['desc'],
            card.get('atk'),
            card.get('def'),
            card.get('level'),
            card['race'],
            card.get('attribute'),
            card.get('archetype'),
            card['card_images'][0].get('image_url'),
            card['card_images'][0].get('image_url_small'),
            card['card_images'][0].get('image_url_cropped')
            )
        card_tuples.append(card_tuple)

    cursor.executemany(insert_query, card_tuples)


def insert_set_table(cursor, card_data):
    insert_query = "INSERT OR IGNORE INTO Card_Set VALUES (?,?,?,?,?,?)"
    set_tuples = []

    for card in card_data['data']:
        if card.get('card_sets'):
            for card_set in card['card_sets']:
                set_tuple = (
                    card['id'],
                    card_set.get('set_name'),
                    card_set.get('set_code'),
                    card_set.get('set_rarity'),
                    card_set.get('set_rarity_code'),
                    card_set.get('set_price')
                )
                set_tuples.append(set_tuple)

    cursor.executemany(insert_query, set_tuples)


def insert_price_table(cursor, card_data):
    insert_query = "INSERT OR IGNORE INTO Card_price VALUES (?,?,?,?,?,?)"
    price_tuples = []

    for card in card_data['data']:
        for card_price in card['card_prices']:
            price_tuple = (
                card['id'],
                card_price['cardmarket_price'],
                card_price['tcgplayer_price'],
                card_price['ebay_price'],
                card_price['amazon_price'],
                card_price['coolstuffinc_price']
            )
            price_tuples.append(price_tuple)

    cursor.executemany(insert_query, price_tuples)


def create_table_data(cursor):

    create_card_table(cursor)
    create_set_table(cursor)
    create_price_table(cursor)


def update_table_data(cursor, card_data):

    insert_card_table(cursor, card_data)
    insert_set_table(cursor, card_data)
    insert_price_table(cursor, card_data)


def main():
    starter = datetime.datetime.now()

    card_api_request(config.DATA_STORAGE_FILE)
    card_data = card_data_request(config.DATA_STORAGE_FILE)
    data_verify.data_print(card_data)

    with sqlite3.connect(config.DATABASE_NAME) as conn:
        cursor = conn.cursor()

        create_table_data(cursor)
        update_table_data(cursor, card_data)
        conn.commit()

        logging.info(f'Table update time: {datetime.datetime.now() - starter}')
        update_time = datetime.datetime.now()

        query = """SELECT DISTINCT * 
                   FROM Cards C 
                   INNER JOIN Card_Set CS on C.id = CS.id 
                   INNER JOIN Card_Price CP ON C.id = CP.id 
                   ORDER BY C.id """

        query_print.query_print(cursor, query)

        logging.info(f'Query execution time: {datetime.datetime.now() - update_time}')
        query_time = datetime.datetime.now()

        query_print.query_pandas(query, conn, config.PANDAS_OUTPUT)
        logging.info(f'Pandas query read time: {datetime.datetime.now() - query_time}')

    logging.info(f'Total time taken: {datetime.datetime.now() - starter}')


if __name__ == '__main__':
    main()
