import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Load dataset
conn = sqlite3.connect("database/netflix.db")

df = pd.read_sql("SELECT * FROM titles", conn)

st.title("🎬 Netflix Data Dashboard")

#filtering by year
st.sidebar.header("Filters")

type_filter = st.sidebar.selectbox("Select Type", ["All", "MOVIE", "SHOW"])

year_filter = st.sidebar.slider(
    "Select Year Range",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2000, 2020)
)

# Applying the filters
filtered_df = df.copy()

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]

filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_filter[0]) &
    (filtered_df['release_year'] <= year_filter[1])
]

st.write("Filtered Titles:", len(filtered_df))

# Overview
st.header("Overview")

st.write("Total Titles:", len(filtered_df))
st.bar_chart(filtered_df['type'].value_counts())

# Ratings
st.header("Ratings Distribution")

fig, ax = plt.subplots()
filtered_df['imdb_score'].hist()
ax.set_title("IMDb Score Distribution")
st.pyplot(fig)

# Content over the years
st.header("Content Growth Over Time")

titles_per_year = filtered_df['release_year'].value_counts().sort_index()

fig2, ax2 = plt.subplots()
titles_per_year.plot(ax=ax2)
ax2.set_title("Titles Released Per Year")

st.pyplot(fig2)

# The top genres
st.header("Top Genres")

genres_df = filtered_df[['id','genres']].copy()
genres_df['genres'] = genres_df['genres'].str.split(', ')
genres_df = genres_df.explode('genres')

top_genres = genres_df['genres'].value_counts().head(10)

st.bar_chart(top_genres)