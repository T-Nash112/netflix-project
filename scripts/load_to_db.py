import pandas as pd
import sqlite3

# Load cleaned data
df = pd.read_csv("data/netflix_titles.csv")

# Recreate normalized tables (same logic you used)
genres_df = df[['id','genres']].copy()
genres_df['genres'] = genres_df['genres'].str.split(', ')
genres_df = genres_df.explode('genres')

countries_df = df[['id','production_countries']].copy()
countries_df['production_countries'] = countries_df['production_countries'].str.split(', ')
countries_df = countries_df.explode('production_countries')

import os
if not os.path.exists('database'):
    os.makedirs('database')
# Create database
conn = sqlite3.connect("database/netflix.db")

# Save tables
df.to_sql("titles", conn, if_exists="replace", index=False)
genres_df.to_sql("genres", conn, if_exists="replace", index=False)
countries_df.to_sql("countries", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")

