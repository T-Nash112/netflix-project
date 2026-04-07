import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/netflix_titles.csv")

st.title("🎬 Netflix Data Dashboard")

# -----------------------------
# Section 1: Overview
# -----------------------------
st.header("Overview")

st.write("Total Titles:", len(df))
st.write("Movies vs Shows:")
st.bar_chart(df['type'].value_counts())

# -----------------------------
# Section 2: Ratings
# -----------------------------
st.header("Ratings Distribution")

fig, ax = plt.subplots()
df['imdb_score'].hist()
ax.set_title("IMDb Score Distribution")
st.pyplot(fig)

# -----------------------------
# Section 3: Content Over Time
# -----------------------------
st.header("Content Growth Over Time")

titles_per_year = df['release_year'].value_counts().sort_index()

fig2, ax2 = plt.subplots()
titles_per_year.plot(ax=ax2)
ax2.set_title("Titles Released Per Year")

st.pyplot(fig2)

#movies vs shows
type_filter = st.selectbox("Select Type", ["All", "MOVIE", "SHOW"])

if type_filter != "All":
    filtered_df = df[df['type'] == type_filter]
else:
    filtered_df = df

#Filtering by year    
year_filter = st.slider(
    "Select Year Range",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2000, 2020)
)

filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_filter[0]) &
    (filtered_df['release_year'] <= year_filter[1])
]

#This is for the top genres
st.header("Top Genres")
genres_df = df[['id','genres']].copy()
genres_df['genres'] = genres_df['genres'].str.split(', ')
genres_df = genres_df.explode('genres')

top_genres = genres_df['genres'].value_counts().head(10)

st.bar_chart(top_genres)