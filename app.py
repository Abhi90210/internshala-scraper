import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import os
from datetime import datetime

st.set_page_config(page_title="Internshala Analyser", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #005EFF;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #0047CC; color: white; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #005EFF; }
    .metric-label { font-size: 0.85rem; color: #666; margin-top: 4px; }
    .hero {
        background: linear-gradient(135deg, #005EFF, #0047CC);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 { font-size: 2.2rem; margin: 0; }
    .hero p { font-size: 1rem; opacity: 0.85; margin-top: 0.5rem; }
    .login-box {
        max-width: 400px;
        margin: 4rem auto;
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #e0e0e0;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #005EFF;
    }
</style>
""", unsafe_allow_html=True)

USERS = {"admin": "intern123", "abhi": "abhi123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login_page():
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem'>
        <h1 style='color:#005EFF'>🎯 Internshala Analyser</h1>
        <p style='color:#666'>Login to explore internship trends</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("### Welcome back!")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong username or password!")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:12px;color:#999;text-align:center'>Demo — username: <b>admin</b> | password: <b>intern123</b></p>", unsafe_allow_html=True)
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
        st.markdown(f"### 👋 Hello, {st.session_state.username}!")
        st.markdown("---")
        page = st.radio("Navigate", ["Dashboard", "Skills Analysis", "Feedback"])
        st.markdown("---")
        locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
        selected_location = st.selectbox("Filter by location", locations)
        min_stipend = st.slider("Min stipend (₹)", 0, 50000, 0, step=1000)
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

    if page == "Dashboard":
        st.markdown("""
        <div class='hero'>
            <h1>🎯 Internshala Skills Analyser</h1>
            <p>Real-time insights from scraped internship listings</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(filtered)}</div><div class='metric-label'>Total Internships</div></div>", unsafe_allow_html=True)
        with c2:
            avg = int(filtered['stipend_clean'].mean()) if filtered['stipend_clean'].notna().any() else 0
            st.markdown(f"<div class='metric-card'><div class='metric-value'>₹{avg:,}</div><div class='metric-label'>Avg Stipend</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{filtered['company'].nunique()}</div><div class='metric-label'>Unique Companies</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(set(all_skills))}</div><div class='metric-label'>Unique Skills</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-title'>Top 10 locations</div>", unsafe_allow_html=True)
            top_loc = filtered["location"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.barh(top_loc.index, top_loc.values, color="#005EFF")
            ax.set_xlabel("Internships")
            ax.spines[['top','right']].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown("<div class='section-title'>Average stipend by city</div>", unsafe_allow_html=True)
            stipend_city = filtered.groupby("location")["stipend_clean"].mean().dropna().sort_values(ascending=False).head(10)
            fig2, ax2 = plt.subplots(figsize=(6,4))
            ax2.barh(stipend_city.index, stipend_city.values, color="#FF6B35")
            ax2.set_xlabel("Avg Stipend (₹)")
            ax2.spines[['top','right']].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig2)

        st.markdown("<div class='section-title'>Top companies hiring</div>", unsafe_allow_html=True)
        top_companies = filtered["company"].value_counts().head(10)
        fig3, ax3 = plt.subplots(figsize=(10,3))
        ax3.bar(top_companies.index, top_companies.values, color="#005EFF")
        ax3.set_ylabel("Listings")
        plt.xticks(rotation=45, ha="right")
        ax3.spines[['top','right']].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig3)

    elif page == "Skills Analysis":
        st.markdown("<h2>Skills Analysis</h2>", unsafe_allow_html=True)

        if all_skills:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='section-title'>Top 20 in-demand skills</div>", unsafe_allow_html=True)
                top_skills = pd.DataFrame(Counter(all_skills).most_common(20), columns=["skill","count"])
                fig, ax = plt.subplots(figsize=(6,7))
                ax.barh(top_skills["skill"][::-1], top_skills["count"][::-1], color="#005EFF")
                ax.set_xlabel("Count")
                ax.spines[['top','right']].set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)

            with col2:
                st.markdown("<div class='section-title'>Skills word cloud</div>", unsafe_allow_html=True)
                wc = WordCloud(width=600, height=500, background_color="white", colormap="Blues", max_words=100).generate(" ".join(all_skills))
                fig2, ax2 = plt.subplots(figsize=(6,7))
                ax2.imshow(wc, interpolation="bilinear")
                ax2.axis("off")
                plt.tight_layout()
                st.pyplot(fig2)

            st.markdown("<div class='section-title'>Raw data</div>", unsafe_allow_html=True)
            st.dataframe(filtered[["title","company","location","stipend","skills"]].reset_index(drop=True), use_container_width=True)

    elif page == "Feedback":
        st.markdown("<h2>Share your feedback</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            name = st.text_input("Your name")
            rating = st.select_slider("Rate this app", options=["⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"], value="⭐⭐⭐")
            feedback = st.text_area("Your feedback", placeholder="What do you think about this app?")
            if st.button("Submit feedback", use_container_width=True):
                if name and feedback:
                    new_row = pd.DataFrame([[name, rating, feedback, datetime.now().strftime("%Y-%m-%d %H:%M")]], columns=["name","rating","feedback","date"])
                    if os.path.exists("feedback.csv"):
                        existing = pd.read_csv("feedback.csv")
                        updated = pd.concat([existing, new_row], ignore_index=True)
                    else:
                        updated = new_row
                    updated.to_csv("feedback.csv", index=False)
                    st.success("Thanks for your feedback!")
                else:
                    st.warning("Please fill in your name and feedback!")

            if os.path.exists("feedback.csv"):
                st.markdown("<div class='section-title'>Recent feedback</div>", unsafe_allow_html=True)
                fb = pd.read_csv("feedback.csv")
                for _, row in fb.iterrows():
                    st.markdown(f"**{row['name']}** {row['rating']} — {row['feedback']} _{row['date']}_")

if st.session_state.logged_in:
    main_app()
else:
    login_page()