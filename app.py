import streamlit as st
import pickle
import pandas as pd

# Page Configuration
st.set_page_config(page_title="CineMatch - Movie Recommendation System", layout="wide")

# Initialize session state for theme (Default: Light/White mode)
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# Top Bar Theme Toggle Button
col_space1, col_space2, col_btn = [st.columns([6, 1, 1])[i] for i in range(3)]
with col_btn:
    if st.session_state.theme == 'Light':
        if st.button("🌙 Dark Mode", use_container_width=True):
            st.session_state.theme = 'Dark'
            st.rerun()
    else:
        if st.button("☀️ Light Mode", use_container_width=True):
            st.session_state.theme = 'Light'
            st.rerun()

# Dynamic Styling based on Theme Selection
if st.session_state.theme == 'Light':
    bg_color = "#FFFFFF"
    text_color = "#1A1A1A"
    sub_text_color = "#555555"
    card_bg = "#F8F9FA"
    card_border = "#E0E0E0"
    card_title_color = "#008736"
    title_gradient = "linear-gradient(135deg, #E60000 0%, #800000 100%)"
    card_hover_border = "#00A844"
else:
    bg_color = "#0d0101"
    text_color = "#FFFFFF"
    sub_text_color = "#C0C0C0"
    card_bg = "linear-gradient(135deg, #031a0b 0%, #072e13 100%)"
    card_border = "#0f4a21"
    card_title_color = "#00FF66"
    title_gradient = "linear-gradient(135deg, #FF3B3B 0%, #FF8080 100%)"
    card_hover_border = "#00FF66"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .main-title {{
        font-size: 3rem;
        background: {title_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }}
    .sub-title {{
        font-size: 1.2rem;
        color: {sub_text_color};
        text-align: center;
        margin-bottom: 30px;
    }}
    .movie-card {{
        background: {card_bg};
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid {card_border};
        transition: all 0.3s ease-in-out;
    }}
    .movie-card:hover {{
        transform: translateY(-5px);
        border-color: {card_hover_border};
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.3);
    }}
    .movie-title {{
        color: {card_title_color};
        font-size: 16px;
        font-weight: 600;
        margin: 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Function to calculate recommendations
def recommend(movie):
    movie_matches = movies[movies['title'].str.lower() == movie.lower()]
    if movie_matches.empty:
        return []
        
    movie_index = movie_matches.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Load dataset and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Landing Page Header
st.markdown('<p class="main-title">CineMatch AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Discover your next favorite movie instantly using Machine Learning and Content-Based Filtering</p>', unsafe_allow_html=True)

st.write("---")

# Centered Search Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        '**Select or type a movie you love:**',
        movies['title'].values
    )
    
    st.write("")
    pressed = st.button('Get Recommendations', use_container_width=True)

# Recommendation Results Section
if pressed:
    with st.spinner('Analyzing movie patterns...'):
        recommendations = recommend(selected_movie_name)
        
    if recommendations:
        st.markdown(f"<br><h3 style='text-align: center; color: {text_color};'>Top Recommended Movies For You</h3><br>", unsafe_allow_html=True)
        
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            if idx < len(recommendations):
                with col:
                    st.markdown(f"""
                        <div class="movie-card">
                            <p class="movie-title">{idx+1}. {recommendations[idx]}</p>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("Movie not found in the dataset!")

# Footer
st.write("<br><br>", unsafe_allow_html=True)
st.write("---")
st.markdown(f"<p style='text-align: center; color: {sub_text_color}; font-size: 13px;'>Developed as a Machine Learning Portfolio Project | Powered by Streamlit and Scikit-Learn</p>", unsafe_allow_html=True)