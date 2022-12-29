import pandas as pd
import sqlite3

df = pd.read_csv("currency_from_api.csv")

connection = sqlite3.connect("currency_from_api.db")
cursor = connection.cursor()
df.to_sql(name="currency_from_api", con=connection, if_exists='replace', index=False)
connection.commit()