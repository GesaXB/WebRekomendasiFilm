import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Custom CSS for modern and interactive styling
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #1e1e2f;
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #a1a1c1;
        }
        /* Hide Streamlit default menu */
        #MainMenu, header, footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Find your next favorite movie, personalized just for you!</p>", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns for movie cards in a single row
    cols = st.columns(5)  # Create 5 columns for displaying recommended movies

    for idx in range(len(recommended_movie_names)):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[idx]}" alt="{recommended_movie_names[idx]} Poster">
                    <p class="movie-title">{recommended_movie_names[idx]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# Footer with copyright
st.markdown(
    """
    <div class="footer">
        © 2024 by Geisha. All Rights Reserved.
    </div>
    """,
    unsafe_allow_html=True
)
