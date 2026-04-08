import sqlite3
import pandas as pd

# Connecting to database
conn = sqlite3.connect("database/netflix.db")

#Checking table
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';", conn
)
print("Tables in database:")
print(tables)

# showing the data (preview)
titles = pd.read_sql("SELECT * FROM titles LIMIT 5;", conn)
print("\nSample data:")
print(titles)

# SQL Queries
# query to check count of Movies vs Shows
query1 = """
SELECT type, COUNT(*) AS total
FROM titles
GROUP BY type;
"""
print("\nMovies vs Shows:")
print(pd.read_sql(query1, conn))

# querying for the Top Rated Titles
query2 = """
SELECT title, imdb_score
FROM titles
ORDER BY imdb_score DESC
LIMIT 10;
"""
print("\nTop Rated Titles:")
print(pd.read_sql(query2, conn))

conn.close()