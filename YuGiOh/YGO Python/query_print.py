import pandas as pd


def query_print(cursor, query):
    cursor.execute(query)
    for card_count in cursor.fetchall():
        print(card_count)
        pass


def query_pandas(query, conn, output_path):
    df = pd.read_sql_query(query, conn)
    df.to_excel(output_path, index=False)
