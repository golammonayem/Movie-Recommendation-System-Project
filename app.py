import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

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

dark = st.session_state.theme == "dark"

if dark:
    PAGE_BG    = "#111116"
    CARD_BG    = "#1C1C23"
    BORDER     = "#2A2A35"
    TEXT_H     = "#F0F0F5"
    TEXT_B     = "#9090A8"
    TEXT_MUTED = "#50505E"
    INPUT_BG   = "#111116"
    DD_BG      = "#1C1C23"
    DD_LI      = "#9090A8"
    DD_HOVER   = "#26262E"
    TOG_BG     = "#1C1C23"
    TOG_FG     = "#9090A8"
    TOG_BORDER = "#2A2A35"
    DIVIDER    = "#1E1E26"
    FOOTER     = "#38383E"
    ICON       = "☀️"
    ICON_LABEL = "Light mode"
else:
    PAGE_BG    = "#F6F6F8"
    CARD_BG    = "#FFFFFF"
    BORDER     = "#E4E4EC"
    TEXT_H     = "#111116"
    TEXT_B     = "#555568"
    TEXT_MUTED = "#AAAAB8"
    INPUT_BG   = "#F6F6F8"
    DD_BG      = "#FFFFFF"
    DD_LI      = "#555568"
    DD_HOVER   = "#F0F0F8"
    TOG_BG     = "#FFFFFF"
    TOG_FG     = "#555568"
    TOG_BORDER = "#E4E4EC"
    DIVIDER    = "#E8E8F0"
    FOOTER     = "#AAAAB8"
    ICON       = "🌙"
    ICON_LABEL = "Dark mode"

ACC = "#E5484D"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {{
    background-color: {PAGE_BG} !important;
    font-family: 'Inter', system-ui, sans-serif;
}}

#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"],
section[data-testid="stSidebar"] {{ display: none !important; }}

.block-container {{
    max-width: 780px !important;
    padding: 0 24px 72px !important;
    margin: 0 auto !important;
}}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] label {{ display: none !important; }}
div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT_H} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    min-height: 44px !important;
    padding: 0 14px !important;
    box-shadow: none !important;
    transition: border-color 0.15s !important;
}}
div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:hover {{
    border-color: {ACC} !important;
}}
div[data-baseweb="select"] svg {{ fill: {TEXT_MUTED} !important; }}
div[data-baseweb="popover"] ul {{
    background: {DD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    padding: 4px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
}}
div[data-baseweb="popover"] li {{
    background: transparent !important;
    color: {DD_LI} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
}}
div[data-baseweb="popover"] li:hover {{
    background: {DD_HOVER} !important;
    color: {TEXT_H} !important;
}}

/* ── Buttons — all default to outline style ── */
div[data-testid="stButton"] > button {{
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    height: 44px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.15s, background 0.15s !important;
    letter-spacing: 0 !important;
    background: {ACC} !important;
    color: #fff !important;
    border: none !important;
    box-shadow: none !important;
    margin-top: 10px !important;
}}
div[data-testid="stButton"] > button:hover {{
    opacity: 0.88 !important;
    transform: none !important;
}}

/* ── Toggle button (theme) — override to look quiet ── */
div[data-testid="stButton"].theme-toggle > button,
#theme-toggle-col div[data-testid="stButton"] > button {{
    background: {TOG_BG} !important;
    color: {TOG_FG} !important;
    border: 1px solid {TOG_BORDER} !important;
    font-size: 12px !important;
    height: 34px !important;
    margin-top: -60px !important;
    box-shadow: none !important;
}}
#theme-toggle-col div[data-testid="stButton"] > button:hover {{
    opacity: 0.8 !important;
}}

/* ── Spinner ── */
div[data-testid="stSpinner"] p {{ color: {TEXT_MUTED} !important; font-size: 14px !important; }}

/* ── Alert ── */
div[data-testid="stAlert"] {{
    background: rgba(229,72,77,0.07) !important;
    border: 1px solid rgba(229,72,77,0.18) !important;
    border-radius: 8px !important;
    color: {ACC} !important;
}}
div[data-testid="stAlert"] p {{ color: {ACC} !important; font-size: 14px !important; }}

/* ── Custom classes ── */
.cm-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 32px 0 0;
    margin-bottom: 52px;
}}
.cm-logo {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT_H};
    display: flex;
    align-items: center;
    gap: 7px;
    letter-spacing: -0.01em;
}}
.cm-logo-mark {{
    width: 7px; height: 7px;
    background: {ACC};
    border-radius: 50%;
    flex-shrink: 0;
}}

.cm-hero {{
    margin-bottom: 40px;
}}
.cm-hero h1 {{
    font-size: clamp(28px, 4.5vw, 46px);
    font-weight: 600;
    color: {TEXT_H};
    line-height: 1.15;
    letter-spacing: -0.025em;
    margin-bottom: 12px;
}}
.cm-hero h1 span {{ color: {ACC}; }}
.cm-hero p {{
    font-size: 15px;
    color: {TEXT_B};
    line-height: 1.6;
    max-width: 400px;
}}

.cm-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 36px;
}}
.cm-label {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_MUTED};
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.cm-results-header {{
    margin-bottom: 16px;
}}
.cm-results-header p {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_MUTED};
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.cm-results-header h2 {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT_H};
    letter-spacing: -0.01em;
}}
.cm-results-header h2 em {{
    color: {ACC};
    font-style: normal;
}}

.cm-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 44px;
}}
.cm-movie-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 16px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 100px;
}}
.cm-movie-card:hover {{
    border-color: {ACC};
}}
.cm-num {{
    font-size: 11px;
    font-weight: 600;
    color: {ACC};
    letter-spacing: 0.08em;
}}
.cm-title {{
    font-size: 13px;
    font-weight: 500;
    color: {TEXT_H};
    line-height: 1.45;
}}

.cm-footer {{
    border-top: 1px solid {DIVIDER};
    padding-top: 20px;
    text-align: center;
    font-size: 12px;
    color: {FOOTER};
}}

@media (max-width: 640px) {{
    .block-container {{ padding: 0 16px 60px !important; }}
    .cm-nav {{ padding-top: 20px; margin-bottom: 36px; }}
    .cm-hero {{ margin-bottom: 28px; }}
    .cm-card {{ padding: 18px; }}
    .cm-grid {{ grid-template-columns: repeat(2, 1fr); gap: 8px; }}
    .cm-movie-card {{ min-height: 80px; padding: 14px 12px; }}
}}
@media (max-width: 400px) {{
    .cm-grid {{ grid-template-columns: 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Nav ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cm-nav">
    <div class="cm-logo">
        <div class="cm-logo-mark"></div>
        CineMatch
    </div>
</div>
""", unsafe_allow_html=True)

# Theme toggle — floated top-right via column trick
_, toggle_col = st.columns([5, 1])
with toggle_col:
    if st.button(f"{ICON}", key="theme_btn", use_container_width=True, help=ICON_LABEL):
        st.session_state.theme = "light" if dark else "dark"
        st.rerun()

# Override toggle button to look quiet
st.markdown(f"""
<style>
button[data-testid="baseButton-secondary"],
div[data-testid="stButton"] button[kind="secondary"] {{
    background: {TOG_BG} !important;
    color: {TOG_FG} !important;
    border: 1px solid {TOG_BORDER} !important;
    font-size: 13px !important;
    height: 32px !important;
    margin-top: -58px !important;
    box-shadow: none !important;
    opacity: 1 !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cm-hero">
    <h1>Find your next<br><span>favorite film</span></h1>
    <p>Pick a movie you love and get five similar picks instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Search ───────────────────────────────────────────────────────────────────
st.markdown('<div class="cm-card">', unsafe_allow_html=True)
st.markdown('<p class="cm-label">Choose a movie</p>', unsafe_allow_html=True)

selected_movie = st.selectbox("Movie", movies['title'].values, label_visibility="collapsed")
pressed = st.button("Find similar movies", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if pressed:
    with st.spinner("Finding matches..."):
        recs = recommend(selected_movie)

    if recs:
        safe = selected_movie.replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"""
<div class="cm-results-header">
    <p>Picks for you</p>
    <h2>Because you liked <em>{safe}</em></h2>
</div>
""", unsafe_allow_html=True)

        nums = ["01", "02", "03", "04", "05"]
        html = '<div class="cm-grid">'
        for i, title in enumerate(recs):
            t = title.replace("<", "&lt;").replace(">", "&gt;")
            html += f"""<div class="cm-movie-card">
    <span class="cm-num">{nums[i]}</span>
    <span class="cm-title">{t}</span>
</div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("Movie not found. Try a different title.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="cm-footer">CineMatch · Content-based filtering · Streamlit & Scikit-Learn</div>', unsafe_allow_html=True)