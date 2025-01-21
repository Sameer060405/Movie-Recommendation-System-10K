import streamlit as st 
import pickle
import pandas as pd 
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import base64
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Retry session setup
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2c8ac926b76413bd376b23868633d1a8'
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
        else:
            return "https://via.placeholder.com/185?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/185?text=Error"

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []

class MovieChatbot:
    def __init__(self, movies_df, similarity_matrix):
        self.movies_df = movies_df
        self.similarity = similarity_matrix
        self.conversation_history = []
        self.user_preferences = {
            'genres': [],
            'era': None,
            'mood': None,
            'rating_min': 0
        }

def set_background(image_file):
    try:
        if not os.path.exists(image_file):
            return
        
        with open(image_file, "rb") as file:
            encoded_image = base64.b64encode(file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_image}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        print(f"Error setting background: {str(e)}")

# Load data
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {str(e)}")
    st.stop()

def main():
    # Set page config
    st.set_page_config(
        page_title="Movie Recommender System",
        page_icon="🎮",
        layout="wide"
    )
    
    # Try to set background
    set_background("hero1.jpg")
    
    # Main title with styling
    st.markdown("""<h1 style='text-align: center;'>🎮 Movie Recommender System</h1>""", unsafe_allow_html=True)
    
    # Initialize session state for chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = MovieChatbot(movies, similarity)  # Fixed: Passing both arguments
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<h3 style='text-align: center;'>Search-Based Recommendations</h3>""", unsafe_allow_html=True)
        
        selected_movie_name = st.selectbox(
            'Select a movie to get recommendations:',
            movies['title'].values
        )
        
        if st.button("🔍 Get Recommendations", key="search_rec"):
            with st.spinner('Finding similar movies...'):
                names, posters = recommend(selected_movie_name)
                if names and posters:
                    movie_cols = st.columns(5)
                    for col, name, poster in zip(movie_cols, names, posters):
                        with col:
                            st.image(poster, use_column_width=True)
                            st.markdown(f"**{name}**")
    
    with col2:
        st.markdown("""<h3 style='text-align: center;'>Chat with Movie Assistant</h3>""", unsafe_allow_html=True)
        
        # Chat history container
        chat_container = st.container()
        
        with chat_container:
            for i, (sender, message) in enumerate(st.session_state.chatbot.conversation_history):
                if sender == 'user':
                    st.markdown(f"<div class='chat-message user-message'><b>You:</b><br>{message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-message bot-message'><b>Assistant:</b><br>{message}</div>", unsafe_allow_html=True)
        
        # Chat input form
        with st.form(key='chat_form', clear_on_submit=True):
            user_message = st.text_input("Type your message:", key="user_input")
            submit_button = st.form_submit_button("Send 💬")
            
            if submit_button and user_message:
                response = st.session_state.chatbot.process_message(user_message)
                st.rerun()

if __name__ == "__main__":
    main()
