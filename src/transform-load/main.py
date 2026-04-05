import pandas as pd
import sqlite3
from datetime import datetime

# Load Json file
df = pd.read_json('data/data.json', lines = False)

# display all collumns
pd.options.display.max_columns = None

# Add data source
df['_source'] = 'https://lista.mercadolivre.com.br/notebook'

# Add pipeline metadata
df['_datetime'] = datetime.now()

# Transform null values
df['old_price'] = df['old_price'].fillna('0')
df['new_price'] = df['new_price'].fillna('0')
df['avg_review'] = df['avg_review'].fillna('0')

# Transform data into strings
df['old_price'] = df['old_price'].astype(str).str.replace('.', '', regex=False)
df['new_price'] = df['new_price'].astype(str).str.replace('.', '', regex=False)

# Clean extra space
df['seller'] = df['seller'].str.strip()

# Convert price columns to float
df['old_price'] = df['old_price'].astype(float)
df['new_price'] = df['new_price'].astype(float)
df['avg_review'] = df['avg_review'].astype(float)

# Calculate discount percentage
df['_discount_pct'] = ((df['old_price'] - df['new_price']) / df['old_price'] * 100).round(2)

# Remove outliers
df = df[
    (df['new_price'] >= 1000) & (df['new_price'] <= 10000) &
    (df['old_price'] >= 1000) & (df['old_price']<= 10000) &
    (df['avg_review'] > 0)
]

print(df)

# Create SQlite database
conn = sqlite3.connect('data/mercadolivre.db')

# Remove duplicates
df = df.drop_duplicates(subset=['name', 'seller'])

# Load data to SQlite
df.to_sql('notebook', conn, if_exists='replace', index=False)

# Close connection 
conn.close()







