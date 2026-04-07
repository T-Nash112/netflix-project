import pandas as pd
import matplotlib.pyplot as plt #this library is for the creation of charts, plots or figures

#Loading the CSV File

df = pd.read_csv("data/netflix_titles.csv")

#Looking at the dataset
df.head()

#checking the info and columns
df.info()
df.describe(include="all")

#Handling missing data or info
df['title'] = df['title'].fillna('Unknown Title')
df['description'] = df['description'].fillna('No Description')
df['age_certification'] = df['age_certification'].fillna('Not Rated')
df['imdb_id'] = df['imdb_id'].fillna('Unknown')

#Filling in the TV SHows and seasons
df.loc[df['type'] =='SHOW','seasons'] = df.loc[df['type']=='SHOW','seasons'].fillna(1)

#verifying if there are still missing values
df.isnull().sum()

#Creating seperate Dataframe for title and genre relationships
genres_df = df[['id','genres']].copy()

#Splitting the comma-seprated genres into lists and explode
genres_df['genres']=genres_df['genres'].str.split(', ')
genres_df = genres_df.explode('genres')

#Stripping the [] blocks
genres_df['genres'] = genres_df['genres'].str.strip('[ ]')

#checking results
genres_df.head()

#do the same for countries
prod_countries_df = df[['id','production_countries']].copy()

prod_countries_df['production_countries'] = prod_countries_df['production_countries'].str.split(', ')
prod_countries_df = prod_countries_df.explode('production_countries')

prod_countries_df['production_countries'] = prod_countries_df['production_countries'].str.strip('[ ]')

prod_countries_df.head()

#Converting Seasons to the datatype Int
df['seasons'].unique()[:20]

df['seasons'] = df['seasons'].round()
df['seasons'] = df['seasons'].astype('Int64')
#showing the change of datatype
df.dtypes

#Making sure movies have no seasons
df.loc[df['type']=='MOVIE','seasons'] = pd.NA

#checking if the previous line worked
df.groupby('type')['seasons'].count()

#checking unique seasons
df.loc[df['type'] == 'SHOW', 'seasons'].unique()

#Checking how many movies and or shows
df['type'].value_counts()

#checking average number of seasons in SHows
df.loc[df['type'] == 'SHOW', 'seasons'].mean()

#checking the show with the highest seasons
df['seasons'].max()

#creating new column for shows
df['is_show'] = df['type'] == 'SHOW'

df[df['is_show']]

#Phase 2 here we do the dataset overview
len(df) #len is a built in function that returns the number of items in an object

df['type'].value_counts()

#Now to draw the chart
df['type'].value_counts().plot(kind='pie')
plt.title('The Number of Movies compared to Shows')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()#there are more movies than shows

#Drawing chart for titles released per year
titles_perYear = df['release_year'].value_counts().sort_index()

titles_perYear.plot(kind='line')
plt.title('The amount of titles per year')
plt.xlabel('Year')
plt.ylabel('Titles')
plt.show()

#Analysing the Ratings
# The top 10 highest rated movies or shows
df.sort_values(by='imdb_score', ascending= False)[['type', 'title', 'imdb_score']].head(10)

#chart for The scores
df['imdb_score'].hist()
plt.title('Score Distribution')
plt.xlabel('imdb_score')
plt.ylabel('Frequency')
plt.show()

#Analysing the SHows
df[df['type'] == 'SHOW']['seasons'].mean() # checking the average seasons a tv show would have

#aranging and showing the shows with the most seasons
df.sort_values(by='seasons',ascending=False)[['type', 'seasons']].head(5)

#this is for runtime analysis for movies
movies = df[df['type'] == 'MOVIE']

movies['runtime'].mean()

movies['runtime'].hist()
plt.title('The Runtime Distribution for movies')
plt.xlabel('Movies (minutes)')
plt.ylabel('Frequency')
plt.show()

#Genre analysis
#top 10 genres
top_n_genres = genres_df['genres'].value_counts().head(10)

top_n_genres.plot(kind='bar')
plt.title('Top genres')
plt.xlabel('Genres')
plt.ylabel('Count')
plt.show()

#correlation between the IMBD AND TMBD
corr =df[['imdb_score', 'tmdb_score']].corr()
print(corr)

#visualizing the correlation
plt.scatter(df['imdb_score'], df['tmdb_score'])
plt.xlabel("IMDb Score")
plt.ylabel("TMDb Score")
plt.title("IMDb Vs TMDb Scores")
plt.show()

#Watching the content growth over time
#very similar to the titles per year
titles_perYear = df['release_year'].value_counts().sort_index()

titles_perYear.plot()
plt.title("Content growth Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.show()

#Movies vs Shows
type_year = df.groupby(['release_year','type']).size().unstack()

type_year.plot()
plt.title("Movies vs Shows Over Time")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

#Checking which countries have the top productions
top_countries = prod_countries_df['production_countries'].value_counts().head(10)

top_countries.plot(kind='bar')
plt.title("Top 10 Production Countries")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.show()

#Highest rated genres
genre_scores = genres_df.merge(df[['id','imdb_score']],on='id')

top_n_genres = genre_scores.groupby('genres')['imdb_score'].mean().sort_values(ascending=False)

top_n_genres.plot(kind='bar')
plt.title("Top Rated Genres")
plt.xlabel("Genre")
plt.ylabel("Average IMDb Score")
plt.show()

#Runtime vs Rating
plt.scatter(df['runtime'], df['imdb_score'])
plt.xlabel("Runtime")
plt.ylabel("IMDb Score")
plt.title("Runtime vs Rating")
plt.show()