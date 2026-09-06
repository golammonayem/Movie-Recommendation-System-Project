import streamlit as st
import pickle
import pandas as pd

# Page Configuration
st.set_page_config(page_title="CineMatch - Movie Recommendation System", page_icon="🎬", layout="wide")

# Custom CSS for Red-Red Gradient Vibe and Glow Hover Effect
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        background: linear-gradient(135deg, #FF1E1E 0%, #800000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #B0B0B0;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-card {
        background: linear-gradient(135deg, #1a0505 0%, #2d0a0a 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
        border: 1px solid #4a0f0f;
        transition: all 0.3s ease-in-out;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: #ff1e1e;
        box-shadow: 0 0 25px rgba(255, 30, 30, 0.8), inset 0 0 10px rgba(255, 30, 30, 0.4);
    }
    .movie-title {
        color: #FFFFFF;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
    }
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
        st.markdown("<br><h3 style='text-align: center; color: #FFFFFF;'>Top Recommended Movies For You</h3><br>", unsafe_allow_html=True)
        
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
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px;'>Developed as a Machine Learning Portfolio Project | Powered by Streamlit and Scikit-Learn</p>", unsafe_allow_html=True)