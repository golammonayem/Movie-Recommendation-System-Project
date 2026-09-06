import streamlit as st
import pickle
import pandas as pd

# Page Configuration
st.set_page_config(page_title="CineMatch - Movie Recommendation System", page_icon="🎬", layout="wide")

# Custom CSS for Landing Page Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #C0C0C0;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 1px solid #333333;
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
st.markdown('<p class="main-title">🎬 CineMatch AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Discover your next favorite movie instantly using Machine Learning & Content-Based Filtering</p>', unsafe_allow_html=True)

st.write("---")

# Centered Search Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        '**Select or type a movie you love:**',
        movies['title'].values
    )
    
    # Spacing and Button
    st.write("")
    pressed = st.button('✨ Get Recommendations', use_container_width=True)

# Recommendation Results Section
if pressed:
    with st.spinner('Analyzing movie patterns and finding best matches...'):
        recommendations = recommend(selected_movie_name)
        
    if recommendations:
        st.markdown("<br><h3 style='text-align: center; color: #FFFFFF;'>🌟 Top 5 Recommended Movies For You</h3><br>", unsafe_allow_html=True)
        
        # Displaying recommendations in a grid of 5 columns
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
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px;'>Developed with ❤️ as a Machine Learning Portfolio Project | Powered by Streamlit & Scikit-Learn</p>", unsafe_allow_html=True)