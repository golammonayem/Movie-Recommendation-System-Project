import streamlit as st
import pickle
import pandas as pd

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch · AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Load Data ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# ─── Recommendation Logic ────────────────────────────────────────────────────────
def recommend(movie):
    matches = movies[movies['title'].str.lower() == movie.lower()]
    if matches.empty:
        return []
    idx = matches.index[0]
    distances = similarity[idx]
    top = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in top]

# ─── Global CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #08080F !important;
    color: #F1FAEE !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none !important; }

/* Remove Streamlit's default gaps */
.stVerticalBlock { gap: 0 !important; }
div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }

/* ── Page Wrapper ── */
.page-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 24px 60px;
    background: #08080F;
}

/* ── Noise texture overlay ── */
.page-wrapper::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

/* ── Top Nav ── */
.nav-bar {
    width: 100%;
    max-width: 1100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 0 0;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
}
.nav-logo {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.12em;
    color: #A8DADC;
    text-transform: uppercase;
}
.nav-tag {
    font-size: 12px;
    color: #4a4a5a;
    font-weight: 400;
    letter-spacing: 0.05em;
}

/* ── Hero ── */
.hero {
    width: 100%;
    max-width: 1100px;
    text-align: center;
    padding: 72px 0 52px;
    position: relative;
    z-index: 1;
}
.hero-eyebrow {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.18em;
    color: #E63946;
    margin-bottom: 20px;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(48px, 7vw, 86px);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #F1FAEE;
    margin-bottom: 22px;
}
.hero-title span {
    color: #E63946;
}
.hero-sub {
    font-size: 17px;
    line-height: 1.65;
    color: #7a7a9a;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
}

/* ── Divider ── */
.divider {
    width: 100%;
    max-width: 1100px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1e2e 30%, #1e1e2e 70%, transparent);
    margin-bottom: 52px;
    position: relative;
    z-index: 1;
}

/* ── Search Section ── */
.search-section {
    width: 100%;
    max-width: 680px;
    position: relative;
    z-index: 1;
    margin-bottom: 56px;
}
.search-label {
    font-size: 13px;
    font-weight: 500;
    color: #7a7a9a;
    margin-bottom: 10px;
    letter-spacing: 0.04em;
}

/* Override Streamlit selectbox */
div[data-testid="stSelectbox"] {
    margin-bottom: 0 !important;
}
div[data-testid="stSelectbox"] > label {
    display: none !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #12121F !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #F1FAEE !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s ease !important;
    box-shadow: 0 0 0 0 transparent !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #E63946 !important;
    box-shadow: 0 0 0 3px rgba(230, 57, 70, 0.12) !important;
}
div[data-testid="stSelectbox"] svg {
    color: #7a7a9a !important;
    fill: #7a7a9a !important;
}

/* Dropdown list */
div[data-baseweb="popover"] {
    background: #12121F !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
div[data-baseweb="popover"] li {
    background: #12121F !important;
    color: #d0d0e0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] {
    background: #1e1e32 !important;
    color: #F1FAEE !important;
}

/* ── Recommend Button ── */
div[data-testid="stButton"] > button {
    background: #E63946 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 14px 28px !important;
    width: 100% !important;
    margin-top: 14px !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.15s ease !important;
    box-shadow: 0 4px 20px rgba(230, 57, 70, 0.25) !important;
}
div[data-testid="stButton"] > button:hover {
    background: #c0282f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(230, 57, 70, 0.35) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Results Section ── */
.results-header {
    width: 100%;
    max-width: 1100px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    z-index: 1;
}
.results-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.16em;
    color: #4a4a5a;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.results-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: #F1FAEE;
}
.results-title span { color: #E63946; }

/* ── Movie Cards ── */
.results-grid {
    width: 100%;
    max-width: 1100px;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    position: relative;
    z-index: 1;
}
.movie-card {
    background: #12121F;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 28px 20px 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 160px;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}
.movie-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #E63946, #A8DADC);
    opacity: 0;
    transition: opacity 0.25s ease;
}
.movie-card:hover {
    border-color: #2e2e48;
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
}
.movie-card:hover::before { opacity: 1; }

.card-rank {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: #E63946;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.card-title {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: #F1FAEE;
    line-height: 1.4;
}

/* ── Footer ── */
.footer {
    width: 100%;
    max-width: 1100px;
    border-top: 1px solid #1a1a2a;
    padding-top: 28px;
    margin-top: 72px;
    text-align: center;
    position: relative;
    z-index: 1;
}
.footer-text {
    font-size: 12px;
    color: #3a3a4e;
    font-weight: 400;
    letter-spacing: 0.04em;
}

/* ── Spinner override ── */
div[data-testid="stSpinner"] {
    color: #E63946 !important;
}

/* ── Warning ── */
div[data-testid="stAlert"] {
    background: #1a0f10 !important;
    border: 1px solid #3e1a1d !important;
    border-radius: 10px !important;
    color: #e07080 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Layout ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# Nav
st.markdown("""
<div class="nav-bar">
    <span class="nav-logo">🎬 CineMatch</span>
    <span class="nav-tag">Content-Based Filtering · ML Powered</span>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <p class="hero-eyebrow">AI-Powered Discovery</p>
    <h1 class="hero-title">Find Your Next<br><span>Favorite Film</span></h1>
    <p class="hero-sub">Tell us a movie you love. Our model analyzes patterns across thousands of films to surface the ones most likely to resonate with you.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Search
st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown('<p class="search-label">Start with a movie you enjoy</p>', unsafe_allow_html=True)

_, center, _ = st.columns([1, 10, 1])
with center:
    selected_movie = st.selectbox(
        "Movie",
        movies['title'].values,
        label_visibility="collapsed",
    )
    pressed = st.button("Find Similar Movies →", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Results
if pressed:
    with st.spinner("Analyzing..."):
        recs = recommend(selected_movie)

    if recs:
        st.markdown("""
        <div class="results-header">
            <p class="results-label">Recommendations for you</p>
            <h2 class="results-title">Because you liked <span>""" + selected_movie + """</span></h2>
        </div>
        """, unsafe_allow_html=True)

        ranks = ["01", "02", "03", "04", "05"]
        cards_html = '<div class="results-grid">'
        for i, title in enumerate(recs):
            cards_html += f"""
            <div class="movie-card">
                <p class="card-rank">Pick {ranks[i]}</p>
                <p class="card-title">{title}</p>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)
    else:
        st.warning("Movie not found in the dataset. Try a different title.")

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">CineMatch · Built with Streamlit & Scikit-Learn · Machine Learning Portfolio Project</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)