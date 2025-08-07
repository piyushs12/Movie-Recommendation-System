import streamlit as st
import pickle
import requests

# Load the saved data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔐 Your TMDb API key here
API_KEY = 'dac3a7936170937e2686633f788dba70'

# Function to fetch poster from TMDb
def fetch_poster(movie_title):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        )
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# Recommender function with posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distance[1:6]:  # Skip the same movie
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

# Streamlit App UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.subheader("🎥 You might like these:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
