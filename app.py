import streamlit as st
import pickle
import pandas as pd

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

# Load the compressed data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit Web UI Design
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie you like, and we will suggest similar ones:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        st.subheader("Top 5 Recommended Movies:")
        for i, rec_movie in enumerate(recommendations, 1):
            st.write(f"{i}. {rec_movie}")
    else:
        st.warning("Movie not found!")