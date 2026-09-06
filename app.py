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
    PAGE_BG = "#111116"
    CARD_BG = "#1C1C23"
    BORDER  = "#2A2A35"
    TEXT_H  = "#F0F0F5"
    TEXT_B  = "#9090A8"
    TEXT_MU = "#50505E"
    INPUT_BG= "#111116"
    DD_BG   = "#1C1C23"
    DD_LI   = "#9090A8"
    DD_HVR  = "#26262E"
    TOG_BG  = "#1C1C23"
    TOG_FG  = "#9090A8"
    TOG_BOR = "#2A2A35"
    DIVIDER = "#1E1E26"
    FOOTER  = "#38383E"
    ICON    = "☀️"
else:
    PAGE_BG = "#F5F5F7"
    CARD_BG = "#FFFFFF"
    BORDER  = "#E4E4EC"
    TEXT_H  = "#111116"
    TEXT_B  = "#555568"
    TEXT_MU = "#AAAAB8"
    INPUT_BG= "#F5F5F7"
    DD_BG   = "#FFFFFF"
    DD_LI   = "#555568"
    DD_HVR  = "#F0F0F8"
    TOG_BG  = "#FFFFFF"
    TOG_FG  = "#555568"
    TOG_BOR = "#E4E4EC"
    DIVIDER = "#E8E8F0"
    FOOTER  = "#AAAAB8"
    ICON    = "🌙"

ACC = "#E5484D"

# Inject CSS in small focused chunks to avoid Streamlit render bug
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)

st.markdown(f"<style>html,body,.stApp,[data-testid='stAppViewContainer'],[data-testid='stMain'],.main{{background-color:{PAGE_BG}!important;font-family:'Inter',system-ui,sans-serif;color:{TEXT_H};}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>#MainMenu,footer,header,.stDeployButton,[data-testid='stToolbar'],[data-testid='stDecoration'],[data-testid='stStatusWidget'],section[data-testid='stSidebar']{{display:none!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>.block-container{{max-width:780px!important;padding:0 24px 72px!important;margin:0 auto!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>div[data-testid='stSelectbox'] label{{display:none!important;}}div[data-testid='stSelectbox']>div>div[data-baseweb='select']>div{{background:{INPUT_BG}!important;border:1px solid {BORDER}!important;border-radius:8px!important;color:{TEXT_H}!important;font-family:'Inter',sans-serif!important;font-size:14px!important;min-height:44px!important;padding:0 14px!important;box-shadow:none!important;}}div[data-testid='stSelectbox']>div>div[data-baseweb='select']>div:hover{{border-color:{ACC}!important;}}div[data-baseweb='select'] svg{{fill:{TEXT_MU}!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>div[data-baseweb='popover'] ul{{background:{DD_BG}!important;border:1px solid {BORDER}!important;border-radius:8px!important;padding:4px!important;}}div[data-baseweb='popover'] li{{background:transparent!important;color:{DD_LI}!important;font-family:'Inter',sans-serif!important;font-size:14px!important;border-radius:6px!important;padding:8px 12px!important;}}div[data-baseweb='popover'] li:hover{{background:{DD_HVR}!important;color:{TEXT_H}!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>div[data-testid='stButton']>button{{font-family:'Inter',sans-serif!important;font-size:14px!important;font-weight:500!important;border-radius:8px!important;height:44px!important;width:100%!important;cursor:pointer!important;background:{ACC}!important;color:#fff!important;border:none!important;box-shadow:none!important;margin-top:10px!important;transition:opacity 0.15s!important;letter-spacing:0!important;}}div[data-testid='stButton']>button:hover{{opacity:0.85!important;transform:none!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"<style>div[data-testid='stSpinner'] p{{color:{TEXT_MU}!important;font-size:14px!important;}}div[data-testid='stAlert']{{background:rgba(229,72,77,0.07)!important;border:1px solid rgba(229,72,77,0.18)!important;border-radius:8px!important;}}div[data-testid='stAlert'] p{{color:{ACC}!important;font-size:14px!important;}}</style>", unsafe_allow_html=True)

st.markdown(f"""<style>
.cm-nav{{display:flex;align-items:center;justify-content:space-between;padding:28px 0 0;margin-bottom:48px;}}
.cm-logo{{font-size:15px;font-weight:600;color:{TEXT_H};display:flex;align-items:center;gap:7px;letter-spacing:-.01em;}}
.cm-dot{{width:7px;height:7px;background:{ACC};border-radius:50%;flex-shrink:0;}}
.cm-tog{{background:{TOG_BG};border:1px solid {TOG_BOR};border-radius:7px;padding:4px 12px;font-size:12px;color:{TOG_FG};cursor:pointer;}}
.cm-hero{{margin-bottom:36px;}}
.cm-hero h1{{font-size:clamp(26px,4.5vw,44px);font-weight:600;color:{TEXT_H};line-height:1.15;letter-spacing:-.025em;margin-bottom:10px;}}
.cm-hero h1 span{{color:{ACC};}}
.cm-hero p{{font-size:15px;color:{TEXT_B};line-height:1.6;max-width:380px;}}
.cm-card{{background:{CARD_BG};border:1px solid {BORDER};border-radius:12px;padding:22px;margin-bottom:32px;}}
.cm-lbl{{font-size:11px;font-weight:600;color:{TEXT_MU};letter-spacing:.07em;text-transform:uppercase;margin-bottom:8px;}}
.cm-rh{{margin-bottom:14px;}}
.cm-rh .cm-rl{{font-size:11px;font-weight:600;color:{TEXT_MU};letter-spacing:.07em;text-transform:uppercase;margin-bottom:4px;}}
.cm-rh h2{{font-size:18px;font-weight:600;color:{TEXT_H};letter-spacing:-.01em;}}
.cm-rh h2 em{{color:{ACC};font-style:normal;}}
.cm-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:40px;}}
.cm-mc{{background:{CARD_BG};border:1px solid {BORDER};border-radius:10px;padding:16px 13px;min-height:96px;display:flex;flex-direction:column;gap:8px;transition:border-color .15s;}}
.cm-mc:hover{{border-color:{ACC};}}
.cm-num{{font-size:11px;font-weight:600;color:{ACC};letter-spacing:.08em;}}
.cm-title{{font-size:13px;font-weight:500;color:{TEXT_H};line-height:1.45;}}
.cm-footer{{border-top:1px solid {DIVIDER};padding-top:18px;text-align:center;font-size:12px;color:{FOOTER};margin-top:4px;}}
@media(max-width:640px){{.block-container{{padding:0 16px 60px!important;}}.cm-nav{{padding-top:20px;margin-bottom:32px;}}.cm-hero{{margin-bottom:24px;}}.cm-card{{padding:18px;}}.cm-grid{{grid-template-columns:repeat(2,1fr);gap:8px;}}.cm-mc{{min-height:76px;padding:13px 11px;}}}}
@media(max-width:360px){{.cm-grid{{grid-template-columns:1fr;}}}}
</style>""", unsafe_allow_html=True)

# ── Nav ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cm-nav">
    <div class="cm-logo"><div class="cm-dot"></div>CineMatch</div>
</div>""", unsafe_allow_html=True)

# Theme toggle
_, tcol = st.columns([5, 1])
with tcol:
    if st.button(ICON, key="tog", use_container_width=True):
        st.session_state.theme = "light" if dark else "dark"
        st.rerun()

st.markdown(f"<style>div[data-testid='stButton']>button[kind]{{background:{TOG_BG}!important;color:{TOG_FG}!important;border:1px solid {TOG_BOR}!important;font-size:13px!important;height:32px!important;margin-top:-54px!important;box-shadow:none!important;}}</style>", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cm-hero">
    <h1>Find your next<br><span>favorite film</span></h1>
    <p>Pick a movie you love and get five similar picks instantly.</p>
</div>""", unsafe_allow_html=True)

# ── Search ───────────────────────────────────────────────────────────────────
st.markdown('<div class="cm-card"><div class="cm-lbl">Choose a movie</div>', unsafe_allow_html=True)
selected_movie = st.selectbox("Movie", movies['title'].values, label_visibility="collapsed")
pressed = st.button("Find similar movies", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if pressed:
    with st.spinner("Finding matches..."):
        recs = recommend(selected_movie)
    if recs:
        safe = selected_movie.replace("<","&lt;").replace(">","&gt;")
        st.markdown(f'<div class="cm-rh"><div class="cm-rl">Picks for you</div><h2>Because you liked <em>{safe}</em></h2></div>', unsafe_allow_html=True)
        nums = ["01","02","03","04","05"]
        html = '<div class="cm-grid">'
        for i, title in enumerate(recs):
            t = title.replace("<","&lt;").replace(">","&gt;")
            html += f'<div class="cm-mc"><span class="cm-num">{nums[i]}</span><span class="cm-title">{t}</span></div>'
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("Movie not found. Try a different title.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="cm-footer">CineMatch · Content-based filtering · Streamlit & Scikit-Learn</div>', unsafe_allow_html=True)