import streamlit as st
import pickle
import pandas as pd
import requests  # For fetching movie posters

# Load Pickle Files
with open("movie_dict.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Convert to DataFrame
movies_df = pd.DataFrame(movies)

# Debugging: Check available columns
#st.write("Movie Data Sample:")
#st.write(movies_df.head())  # Debugging to check column names

# Function to Fetch Poster from TMDb API
API_KEY = "be19d38685d740cf50d790d1def479ef"


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    if "poster_path" in data and data["poster_path"]:
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return None


# Recommendation Function
def recommend(movie):
    if movie not in movies_df["title"].values:
        return ["Movie not found in database"], []

    index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in recommended:
        movie_title = movies_df.iloc[i[0]].title

        # Use correct column name
        movie_id = movies_df.iloc[i[0]].get("movie_id", None)  # Use correct column
        if movie_id is None:
            continue  # Skip if no movie_id available

        poster_url = fetch_poster(movie_id)

        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters


# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie:", movies_df["title"].values)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)

    st.subheader("Recommended Movies:")

    cols = st.columns(5)  # Create 5 columns for movie posters
    for i in range(len(recommendations)):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.write(recommendations[i])
