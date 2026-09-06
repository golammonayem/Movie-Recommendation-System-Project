import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="CineMatch — Movie Recommendations",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

def recommend(movie):
    matches = movies[movies['title'].str.lower() == movie.lower()]
    if matches.empty:
        return []
    idx = matches.index[0]
    distances = similarity[idx]
    top = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in top]

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #0C0C14;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
section[data-testid="stSidebar"] { display: none !important; }

.block-container {
    max-width: 860px !important;
    padding: 0 20px 80px !important;
    margin: 0 auto !important;
}

.cm-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 0 0;
    margin-bottom: 64px;
}
.cm-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.01em;
}
.cm-logo-dot {
    width: 8px;
    height: 8px;
    background: #E5484D;
    border-radius: 50%;
}
.cm-badge {
    font-size: 11px;
    font-weight: 500;
    color: #E5484D;
    background: rgba(229, 72, 77, 0.12);
    border: 1px solid rgba(229, 72, 77, 0.22);
    border-radius: 20px;
    padding: 3px 10px;
    letter-spacing: 0.02em;
}

.cm-hero {
    text-align: center;
    margin-bottom: 52px;
}
.cm-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 6vw, 64px);
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.1;
    letter-spacing: -0.025em;
    margin: 0 0 16px;
}
.cm-hero-title em {
    color: #E5484D;
    font-style: normal;
}
.cm-hero-sub {
    font-size: 16px;
    color: #6B6B80;
    line-height: 1.6;
    max-width: 460px;
    margin: 0 auto;
    font-weight: 400;
}

.cm-search-card {
    background: #13131F;
    border: 1px solid #1E1E2E;
    border-radius: 16px;
    padding: 28px 28px 24px;
    margin-bottom: 48px;
}
.cm-search-label {
    font-size: 12px;
    font-weight: 500;
    color: #4A4A5E;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

div[data-testid="stSelectbox"] label { display: none !important; }

div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div {
    background: #0C0C14 !important;
    border: 1px solid #252535 !important;
    border-radius: 10px !important;
    color: #E8E8F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    min-height: 48px !important;
    padding: 0 16px !important;
    transition: border-color 0.18s ease !important;
}
div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:hover {
    border-color: #E5484D !important;
}
div[data-baseweb="select"] svg { fill: #4A4A5E !important; }

div[data-baseweb="popover"] ul {
    background: #13131F !important;
    border: 1px solid #252535 !important;
    border-radius: 10px !important;
    padding: 6px !important;
}
div[data-baseweb="popover"] li {
    background: transparent !important;
    color: #B0B0C4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
}
div[data-baseweb="popover"] li:hover {
    background: #1E1E30 !important;
    color: #FFFFFF !important;
}

div[data-testid="stButton"] > button {
    background: #E5484D !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    height: 48px !important;
    width: 100% !important;
    margin-top: 12px !important;
    cursor: pointer !important;
    transition: opacity 0.18s ease, transform 0.12s ease !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active {
    opacity: 1 !important;
    transform: translateY(0) !important;
}

.cm-results-heading {
    font-size: 13px;
    font-weight: 500;
    color: #4A4A5E;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.cm-results-heading span {
    color: #E5484D;
    text-transform: none;
    letter-spacing: 0;
    font-style: italic;
}

.cm-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
    gap: 12px;
    margin-bottom: 48px;
}
.cm-card {
    background: #13131F;
    border: 1px solid #1E1E2E;
    border-radius: 12px;
    padding: 20px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: border-color 0.2s ease, transform 0.2s ease;
    min-height: 140px;
}
.cm-card:hover {
    border-color: #2E2E48;
    transform: translateY(-3px);
}
.cm-card-num {
    font-size: 11px;
    font-weight: 600;
    color: #E5484D;
    letter-spacing: 0.1em;
}
.cm-card-title {
    font-size: 14px;
    font-weight: 500;
    color: #E8E8F0;
    line-height: 1.45;
    flex: 1;
}

.cm-divider {
    height: 1px;
    background: #1A1A28;
    margin: 0 0 28px;
}
.cm-footer {
    text-align: center;
    font-size: 12px;
    color: #2E2E44;
    padding-bottom: 16px;
}

div[data-testid="stSpinner"] p { color: #6B6B80 !important; }

div[data-testid="stAlert"] {
    background: rgba(229, 72, 77, 0.08) !important;
    border: 1px solid rgba(229, 72, 77, 0.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stAlert"] p { color: #F0A0A2 !important; }

@media (max-width: 600px) {
    .block-container { padding: 0 16px 60px !important; }
    .cm-nav { margin-bottom: 40px; padding-top: 20px; }
    .cm-hero { margin-bottom: 36px; }
    .cm-search-card { padding: 20px; }
    .cm-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
    .cm-card { min-height: 110px; padding: 16px 14px; }
}
@media (max-width: 380px) {
    .cm-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cm-nav">
    <div class="cm-logo">
        <div class="cm-logo-dot"></div>
        CineMatch
    </div>
    <span class="cm-badge">ML Powered</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cm-hero">
    <h1 class="cm-hero-title">Find your next<br><em>favorite film</em></h1>
    <p class="cm-hero-sub">Pick a movie you love. Our content-based model finds the five most similar films for you.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cm-search-card">', unsafe_allow_html=True)
st.markdown('<p class="cm-search-label">Choose a movie</p>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Movie",
    movies['title'].values,
    label_visibility="collapsed",
)
pressed = st.button("Find similar movies", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if pressed:
    with st.spinner("Finding recommendations..."):
        recs = recommend(selected_movie)

    if recs:
        safe_title = selected_movie.replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(
            f'<p class="cm-results-heading">Because you liked <span>{safe_title}</span></p>',
            unsafe_allow_html=True
        )
        nums = ["01", "02", "03", "04", "05"]
        cards_html = '<div class="cm-grid">'
        for i, title in enumerate(recs):
            safe = title.replace("<", "&lt;").replace(">", "&gt;")
            cards_html += f"""
            <div class="cm-card">
                <span class="cm-card-num">{nums[i]}</span>
                <span class="cm-card-title">{safe}</span>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
    else:
        st.warning("Movie not found. Try a different title.")

st.markdown('<div class="cm-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="cm-footer">CineMatch · Content-Based Filtering · Built with Streamlit & Scikit-Learn</p>',
    unsafe_allow_html=True
)