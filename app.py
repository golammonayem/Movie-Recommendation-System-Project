import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="CineMatch — Movie Recommendations",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Session state: theme ─────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── Data ─────────────────────────────────────────────────────────────────────
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

# ── Theme tokens ─────────────────────────────────────────────────────────────
is_dark = st.session_state.theme == "dark"

if is_dark:
    T = {
        "app_bg":        "#0C0C14",
        "surface":       "#13131F",
        "surface2":      "#0C0C14",
        "border":        "#1E1E2E",
        "border2":       "#252535",
        "text_primary":  "#EEEEF5",
        "text_secondary":"#6B6B80",
        "text_muted":    "#3A3A52",
        "text_label":    "#4A4A5E",
        "dropdown_li":   "#B0B0C4",
        "dropdown_li_hover_bg": "#1E1E30",
        "logo_color":    "#FFFFFF",
        "card_hover_border": "#2E2E48",
        "footer_color":  "#2E2E44",
        "spinner_color": "#6B6B80",
        "divider":       "#1A1A28",
        "toggle_bg":     "#1E1E2E",
        "toggle_color":  "#B0B0C4",
        "toggle_hover":  "#252535",
        "icon":          "☀️",
        "icon_label":    "Light",
    }
else:
    T = {
        "app_bg":        "#F5F5F7",
        "surface":       "#FFFFFF",
        "surface2":      "#F0F0F4",
        "border":        "#E2E2EA",
        "border2":       "#D4D4DF",
        "text_primary":  "#111118",
        "text_secondary":"#555568",
        "text_muted":    "#AAAABC",
        "text_label":    "#888898",
        "dropdown_li":   "#444455",
        "dropdown_li_hover_bg": "#F0F0F8",
        "logo_color":    "#111118",
        "card_hover_border": "#CBCBDF",
        "footer_color":  "#AAAABC",
        "spinner_color": "#888898",
        "divider":       "#E2E2EA",
        "toggle_bg":     "#E8E8F0",
        "toggle_color":  "#444455",
        "toggle_hover":  "#DDDDE8",
        "icon":          "🌙",
        "icon_label":    "Dark",
    }

ACCENT = "#E5484D"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp {{
    background-color: {T['app_bg']} !important;
    font-family: 'Inter', sans-serif;
    color: {T['text_primary']};
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"],
section[data-testid="stSidebar"] {{ display: none !important; }}

/* Wipe Streamlit's default white bg */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{ background-color: {T['app_bg']} !important; }}

.block-container {{
    max-width: 860px !important;
    padding: 0 24px 80px !important;
    margin: 0 auto !important;
}}

/* ── Nav ── */
.cm-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 0 0;
    margin-bottom: 60px;
}}
.cm-logo {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: {T['logo_color']};
    letter-spacing: -0.01em;
}}
.cm-logo-dot {{
    width: 8px;
    height: 8px;
    background: {ACCENT};
    border-radius: 50%;
    flex-shrink: 0;
}}
.cm-nav-right {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.cm-badge {{
    font-size: 11px;
    font-weight: 500;
    color: {ACCENT};
    background: rgba(229, 72, 77, 0.10);
    border: 1px solid rgba(229, 72, 77, 0.22);
    border-radius: 20px;
    padding: 4px 10px;
    letter-spacing: 0.02em;
    white-space: nowrap;
}}

/* ── Theme toggle ── */
.cm-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {T['toggle_bg']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 500;
    color: {T['toggle_color']};
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.15s ease;
    text-decoration: none;
}}
.cm-toggle:hover {{ background: {T['toggle_hover']}; }}

/* ── Hero ── */
.cm-hero {{
    text-align: center;
    margin-bottom: 48px;
}}
.cm-hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(34px, 5.5vw, 60px);
    font-weight: 700;
    color: {T['text_primary']};
    line-height: 1.1;
    letter-spacing: -0.025em;
    margin-bottom: 14px;
}}
.cm-hero-title em {{
    color: {ACCENT};
    font-style: normal;
}}
.cm-hero-sub {{
    font-size: 15px;
    color: {T['text_secondary']};
    line-height: 1.65;
    max-width: 440px;
    margin: 0 auto;
}}

/* ── Search card ── */
.cm-search-card {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    padding: 28px 28px 24px;
    margin-bottom: 44px;
}}
.cm-search-label {{
    font-size: 11px;
    font-weight: 600;
    color: {T['text_label']};
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 10px;
}}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] label {{ display: none !important; }}

div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border2']} !important;
    border-radius: 10px !important;
    color: {T['text_primary']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    min-height: 48px !important;
    padding: 0 16px !important;
    transition: border-color 0.18s ease !important;
}}
div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:hover {{
    border-color: {ACCENT} !important;
}}
div[data-baseweb="select"] svg {{ fill: {T['text_label']} !important; }}

div[data-baseweb="popover"] ul {{
    background: {T['surface']} !important;
    border: 1px solid {T['border2']} !important;
    border-radius: 10px !important;
    padding: 6px !important;
}}
div[data-baseweb="popover"] li {{
    background: transparent !important;
    color: {T['dropdown_li']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
}}
div[data-baseweb="popover"] li:hover {{
    background: {T['dropdown_li_hover_bg']} !important;
    color: {T['text_primary']} !important;
}}

/* ── Main button ── */
div[data-testid="stButton"] > button {{
    background: {ACCENT} !important;
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
    transition: opacity 0.15s ease, transform 0.12s ease !important;
    box-shadow: 0 2px 12px rgba(229, 72, 77, 0.28) !important;
}}
div[data-testid="stButton"] > button:hover {{
    opacity: 0.87 !important;
    transform: translateY(-1px) !important;
}}
div[data-testid="stButton"] > button:active {{
    opacity: 1 !important;
    transform: translateY(0) !important;
}}

/* ── Results heading ── */
.cm-results-label {{
    font-size: 11px;
    font-weight: 600;
    color: {T['text_label']};
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.cm-results-title {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: {T['text_primary']};
    margin-bottom: 20px;
    line-height: 1.3;
}}
.cm-results-title em {{
    color: {ACCENT};
    font-style: normal;
}}

/* ── Cards grid ── */
.cm-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 52px;
}}
.cm-card {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 20px 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}}
.cm-card:hover {{
    border-color: {T['card_hover_border']};
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}}
.cm-card-num {{
    font-size: 11px;
    font-weight: 700;
    color: {ACCENT};
    letter-spacing: 0.1em;
}}
.cm-card-title {{
    font-size: 13px;
    font-weight: 500;
    color: {T['text_primary']};
    line-height: 1.5;
}}

/* ── Divider & footer ── */
.cm-divider {{
    height: 1px;
    background: {T['divider']};
    margin: 0 0 24px;
}}
.cm-footer {{
    text-align: center;
    font-size: 12px;
    color: {T['footer_color']};
    padding-bottom: 12px;
}}

/* ── Spinner & alert ── */
div[data-testid="stSpinner"] p {{ color: {T['spinner_color']} !important; }}
div[data-testid="stAlert"] {{
    background: rgba(229,72,77,0.07) !important;
    border: 1px solid rgba(229,72,77,0.2) !important;
    border-radius: 10px !important;
}}
div[data-testid="stAlert"] p {{ color: #E5484D !important; }}

/* ── Responsive ── */
@media (max-width: 720px) {{
    .cm-grid {{ grid-template-columns: repeat(3, 1fr); }}
}}
@media (max-width: 540px) {{
    .block-container {{ padding: 0 16px 60px !important; }}
    .cm-nav {{ margin-bottom: 40px; padding-top: 20px; }}
    .cm-hero {{ margin-bottom: 32px; }}
    .cm-search-card {{ padding: 20px 18px; }}
    .cm-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
    .cm-badge {{ display: none; }}
}}
@media (max-width: 360px) {{
    .cm-grid {{ grid-template-columns: 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Nav (HTML) ────────────────────────────────────────────────────────────────
icon = T['icon']
icon_label = T['icon_label']

st.markdown(f"""
<div class="cm-nav">
    <div class="cm-logo">
        <div class="cm-logo-dot"></div>
        CineMatch
    </div>
    <div class="cm-nav-right">
        <span class="cm-badge">ML Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Theme toggle button — placed AFTER nav HTML so it flows in the same visual area
# We use a Streamlit column trick to float it to the right
_left, _right = st.columns([6, 1])
with _right:
    toggle_label = f"{T['icon']} {T['icon_label']}"
    if st.button(toggle_label, key="theme_btn", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

# Override toggle button style to look like our cm-toggle
st.markdown(f"""
<style>
div[data-testid="stButton"][id*="theme_btn"] > button,
button[kind="secondary"][data-testid="baseButton-secondary"] {{
    background: {T['toggle_bg']} !important;
    color: {T['toggle_color']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    height: 34px !important;
    letter-spacing: 0 !important;
    box-shadow: none !important;
    margin-top: -64px !important;
}}
div[data-testid="stButton"][id*="theme_btn"] > button:hover {{
    background: {T['toggle_hover']} !important;
    opacity: 1 !important;
    transform: none !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cm-hero">
    <h1 class="cm-hero-title">Find your next<br><em>favorite film</em></h1>
    <p class="cm-hero-sub">Pick a movie you love — our content-based model finds the five most similar films instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Search card ───────────────────────────────────────────────────────────────
st.markdown('<div class="cm-search-card">', unsafe_allow_html=True)
st.markdown('<p class="cm-search-label">Choose a movie you love</p>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Movie",
    movies['title'].values,
    label_visibility="collapsed",
)
pressed = st.button("Find similar movies", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if pressed:
    with st.spinner("Analyzing patterns..."):
        recs = recommend(selected_movie)

    if recs:
        safe_title = selected_movie.replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"""
<p class="cm-results-label">Recommended for you</p>
<p class="cm-results-title">Because you liked <em>{safe_title}</em></p>
""", unsafe_allow_html=True)

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
        st.warning("Movie not found in the dataset. Try a different title.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="cm-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="cm-footer">CineMatch · Content-Based Filtering · Streamlit & Scikit-Learn</p>',
    unsafe_allow_html=True
)