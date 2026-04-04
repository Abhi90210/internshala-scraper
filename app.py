import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import os
from datetime import datetime

st.set_page_config(page_title="InternIQ", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] { background: #F0F4FF; }
[data-testid="stSidebar"] { background: #1A1F5E !important; }
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stRadio label { 
    background: rgba(255,255,255,0.08); 
    border-radius: 10px; padding: 0.6rem 1rem; 
    margin-bottom: 6px; display: block;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.18); }
.stButton>button {
    background: linear-gradient(135deg, #4F6EF7, #1A1F5E);
    color: white !important; border: none;
    border-radius: 10px; padding: 0.55rem 1.5rem;
    font-weight: 600; font-size: 0.95rem;
    transition: all 0.2s; width: 100%;
}
.stButton>button:hover { opacity: 0.88; transform: translateY(-1px); }

.hero {
    background: linear-gradient(135deg, #1A1F5E 0%, #4F6EF7 100%);
    border-radius: 20px; padding: 2.5rem 2rem;
    color: white; text-align: center;
    animation: fadeInDown 0.6s ease;
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 2.4rem; font-weight: 700; margin: 0; }
.hero p { font-size: 1rem; opacity: 0.8; margin-top: 0.4rem; }

.metric-card {
    background: white; border-radius: 16px;
    padding: 1.4rem; text-align: center;
    border: 1px solid #E8EDFF;
    animation: fadeInUp 0.5s ease;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-value { font-size: 2rem; font-weight: 700; color: #4F6EF7; }
.metric-label { font-size: 0.82rem; color: #888; margin-top: 4px; font-weight: 500; }

.section-card {
    background: white; border-radius: 16px;
    padding: 1.5rem; border: 1px solid #E8EDFF;
    margin-bottom: 1rem; animation: fadeInUp 0.5s ease;
}
.section-title {
    font-size: 1.05rem; font-weight: 700;
    color: #1A1F5E; margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #4F6EF7;
}

.login-wrap {
    min-height: 100vh; display: flex;
    align-items: center; justify-content: center;
}
.login-card {
    background: white; border-radius: 20px;
    padding: 2.5rem; width: 100%; max-width: 400px;
    border: 1px solid #E8EDFF;
    animation: fadeInUp 0.6s ease;
}
.login-title { font-size: 1.6rem; font-weight: 700; color: #1A1F5E; text-align: center; margin-bottom: 0.3rem; }
.login-sub { font-size: 0.88rem; color: #888; text-align: center; margin-bottom: 1.5rem; }

.tag {
    display: inline-block; background: #EEF2FF;
    color: #4F6EF7; border-radius: 20px;
    padding: 3px 12px; font-size: 0.78rem;
    font-weight: 600; margin: 2px;
}

.feedback-card {
    background: #F8F9FF; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 10px;
    border-left: 4px solid #4F6EF7;
    animation: fadeInUp 0.4s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
.loading { animation: pulse 1.5s infinite; color: #4F6EF7; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

USERS = {"admin": "intern123", "abhi": "abhi123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login_page():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 3rem 0 1.5rem'>
            <div style='font-size:3rem'>🎯</div>
            <h1 style='color:#1A1F5E; font-size:2rem; margin:0'>InternIQ</h1>
            <p style='color:#888; margin-top:0.3rem'>Your internship market intelligence tool</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown("<p class='login-title'>Welcome back 👋</p>", unsafe_allow_html=True)
            st.markdown("<p class='login-sub'>Login to explore real internship insights</p>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login →"):
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logging you in...")
                    st.rerun()
                else:
                    st.error("Wrong username or password. Try again!")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background:#F0F4FF; border-radius:10px; padding:10px 14px; font-size:12px; color:#666;'>
                Demo credentials<br>
                Username: <b>admin</b> &nbsp;|&nbsp; Password: <b>intern123</b>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

def main_app():
    df = pd.read_csv("internships.csv")

    def clean_stipend(s):
        try:
            s = s.replace("₹","").replace("/month","").replace(",","").strip()
            if "-" in s:
                parts = s.split("-")
                return (int(parts[0].strip()) + int(parts[1].strip())) / 2
            return float(s.strip())
        except:
            return None

    df["stipend_clean"] = df["stipend"].apply(clean_stipend)

    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding: 1rem 0 0.5rem'>
            <div style='font-size:2rem'>🎯</div>
            <p style='font-size:1.1rem; font-weight:700; margin:0'>InternIQ</p>
            <p style='font-size:0.8rem; opacity:0.6; margin:0'>Hello, {st.session_state.username}!</p>
        </div>
        <hr style='border-color:rgba(255,255,255,0.15); margin: 1rem 0'>
        """, unsafe_allow_html=True)

        page = st.radio("", ["🏠  Dashboard", "🔍  Skills Analysis", "📊  Data Explorer", "💬  Feedback"])
        st.markdown("<hr style='border-color:rgba(255,255,255,0.15)'>", unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.8rem; opacity:0.6; font-weight:600'>FILTERS</p>", unsafe_allow_html=True)
        locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
        selected_location = st.selectbox("Location", locations)
        min_stipend = st.slider("Min stipend (₹)", 0, 50000, 0, step=1000)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    filtered = df.copy()
    if selected_location != "All":
        filtered = filtered[filtered["location"] == selected_location]
    filtered = filtered[filtered["stipend_clean"].fillna(0) >= min_stipend]

    all_skills = []
    for s in filtered["skills"].dropna():
        if s != "N/A":
            all_skills.extend([x.strip() for x in s.split(",")])

    if "🏠" in page:
        st.markdown("""
        <div class='hero'>
            <h1>🎯 Internshala Market Intelligence</h1>
            <p>Analysing real internship listings scraped live from Internshala</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        avg = int(filtered['stipend_clean'].mean()) if filtered['stipend_clean'].notna().any() else 0
        for col, val, label in zip(
            [c1, c2, c3, c4],
            [len(filtered), f"₹{avg:,}", filtered['company'].nunique(), len(set(all_skills))],
            ["Internships", "Avg Stipend", "Companies", "Unique Skills"]
        ):
            with col:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-card'><div class='section-title'>Top locations</div>", unsafe_allow_html=True)
            top_loc = filtered["location"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(6, 4))
            bars = ax.barh(top_loc.index[::-1], top_loc.values[::-1], color="#4F6EF7", edgecolor="none")
            ax.set_xlabel("Internships", color="#888")
            ax.spines[['top','right','left']].set_visible(False)
            ax.tick_params(colors='#555')
            fig.patch.set_facecolor('white')
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-card'><div class='section-title'>Avg stipend by city</div>", unsafe_allow_html=True)
            stipend_city = filtered.groupby("location")["stipend_clean"].mean().dropna().sort_values(ascending=False).head(10)
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.barh(stipend_city.index[::-1], stipend_city.values[::-1], color="#FF6B35", edgecolor="none")
            ax2.set_xlabel("Avg Stipend (₹)", color="#888")
            ax2.spines[['top','right','left']].set_visible(False)
            ax2.tick_params(colors='#555')
            fig2.patch.set_facecolor('white')
            plt.tight_layout()
            st.pyplot(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><div class='section-title'>Top hiring companies</div>", unsafe_allow_html=True)
        top_co = filtered["company"].value_counts().head(12)
        fig3, ax3 = plt.subplots(figsize=(10, 3))
        ax3.bar(top_co.index, top_co.values, color="#4F6EF7", edgecolor="none")
        ax3.set_ylabel("Listings", color="#888")
        ax3.spines[['top','right']].set_visible(False)
        ax3.tick_params(colors='#555')
        plt.xticks(rotation=35, ha="right", fontsize=9)
        fig3.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig3)
        st.markdown("</div>", unsafe_allow_html=True)

    elif "🔍" in page:
        st.markdown("<h2 style='color:#1A1F5E'>Skills Analysis</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888'>What skills are companies actually looking for?</p>", unsafe_allow_html=True)

        if all_skills:
            skill_counts = Counter(all_skills)
            top_skills = pd.DataFrame(skill_counts.most_common(20), columns=["skill","count"])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='section-card'><div class='section-title'>Top 20 in-demand skills</div>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(6, 7))
                colors = ["#4F6EF7" if i < 3 else "#A5B4FC" for i in range(len(top_skills))]
                ax.barh(top_skills["skill"][::-1], top_skills["count"][::-1], color=colors[::-1], edgecolor="none")
                ax.set_xlabel("Mentions", color="#888")
                ax.spines[['top','right','left']].set_visible(False)
                ax.tick_params(colors='#555')
                fig.patch.set_facecolor('white')
                plt.tight_layout()
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='section-card'><div class='section-title'>Skills word cloud</div>", unsafe_allow_html=True)
                wc = WordCloud(
                    width=600, height=560,
                    background_color="white",
                    colormap="cool",
                    max_words=80,
                    prefer_horizontal=0.9
                ).generate(" ".join(all_skills))
                fig2, ax2 = plt.subplots(figsize=(6, 7))
                ax2.imshow(wc, interpolation="bilinear")
                ax2.axis("off")
                fig2.patch.set_facecolor('white')
                plt.tight_layout()
                st.pyplot(fig2)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'><div class='section-title'>Top skill tags</div>", unsafe_allow_html=True)
            tags_html = " ".join([f"<span class='tag'>{s} ({c})</span>" for s, c in skill_counts.most_common(30)])
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif "📊" in page:
        st.markdown("<h2 style='color:#1A1F5E'>Data Explorer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888'>Browse and search through all scraped internship listings</p>", unsafe_allow_html=True)

        search = st.text_input("Search by title or company", placeholder="e.g. Python, Marketing, Mumbai...")
        if search:
            display = filtered[
                filtered["title"].str.contains(search, case=False, na=False) |
                filtered["company"].str.contains(search, case=False, na=False)
            ]
        else:
            display = filtered

        st.markdown(f"<p style='color:#888; font-size:0.88rem'>Showing {len(display)} listings</p>", unsafe_allow_html=True)
        st.dataframe(
            display[["title","company","location","stipend","skills"]].reset_index(drop=True),
            use_container_width=True, height=420
        )

    elif "💬" in page:
        st.markdown("<h2 style='color:#1A1F5E'>Feedback</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888'>Help improve this app — your feedback matters!</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            name = st.text_input("Your name", placeholder="Enter your name")
            rating = st.select_slider("Rating", options=["⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"], value="⭐⭐⭐⭐")
            feedback = st.text_area("Your feedback", placeholder="What did you like? What can be improved?", height=120)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Submit feedback →"):
                if name and feedback:
                    new_row = pd.DataFrame([[name, rating, feedback, datetime.now().strftime("%d %b %Y, %H:%M")]], columns=["name","rating","feedback","date"])
                    if os.path.exists("feedback.csv"):
                        updated = pd.concat([pd.read_csv("feedback.csv"), new_row], ignore_index=True)
                    else:
                        updated = new_row
                    updated.to_csv("feedback.csv", index=False)
                    st.success("Thanks for your feedback! 🎉")
                    st.balloons()
                else:
                    st.warning("Please fill in your name and feedback!")
            st.markdown("</div>", unsafe_allow_html=True)

        if os.path.exists("feedback.csv"):
            fb = pd.read_csv("feedback.csv")
            if len(fb) > 0:
                st.markdown("<br><div class='section-title'>Recent feedback</div>", unsafe_allow_html=True)
                for _, row in fb.iloc[::-1].iterrows():
                    st.markdown(f"""
                    <div class='feedback-card'>
                        <b>{row['name']}</b> &nbsp; {row['rating']} &nbsp;
                        <span style='font-size:0.8rem; color:#888'>{row['date']}</span><br>
                        <span style='color:#333; font-size:0.92rem'>{row['feedback']}</span>
                    </div>
                    """, unsafe_allow_html=True)

if st.session_state.logged_in:
    main_app()
else:
    login_page()