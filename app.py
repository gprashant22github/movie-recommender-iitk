import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
with open("movie_dict.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

movies_df = pd.DataFrame(movies)

# TMDB API Key
API_KEY = "91daf36aedbec8a6ae6e6ed7bf362446"

# Fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    except:
        pass
    # Fallback image
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend function
def recommend(movie):
    if movie not in movies_df["title"].values:
        return ["Movie not found"], []

    index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in recommended:
        movie_id = movies_df.iloc[i[0]]["movie_id"]
        poster = fetch_poster(movie_id)
        recommended_movies.append(movies_df.iloc[i[0]]["title"])
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie:", movies_df["title"].values)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)

    st.subheader("Recommended Movies:")
    cols = st.columns(5)
    for i in range(len(recommendations)):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(recommendations[i])
