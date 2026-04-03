import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

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

st.title("Internshala Skills Analyser")
st.write(f"Analysing {len(df)} internship listings")

locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
selected_location = st.selectbox("Filter by location", locations)

if selected_location != "All":
    filtered = df[df["location"] == selected_location]
else:
    filtered = df

col1, col2, col3 = st.columns(3)
col1.metric("Total Internships", len(filtered))
col2.metric("Avg Stipend", f"₹{int(filtered['stipend_clean'].mean()):,}" if filtered['stipend_clean'].notna().any() else "N/A")
col3.metric("Unique Companies", filtered["company"].nunique())

st.subheader("Top 20 in-demand skills")
all_skills = []
for s in filtered["skills"].dropna():
    if s != "N/A":
        all_skills.extend([x.strip() for x in s.split(",")])

if all_skills:
    top_skills = pd.DataFrame(Counter(all_skills).most_common(20), columns=["skill","count"])
    fig, ax = plt.subplots(figsize=(8,6))
    ax.barh(top_skills["skill"], top_skills["count"], color="steelblue")
    ax.set_xlabel("Count")
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Skills word cloud")
if all_skills:
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(all_skills))
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.imshow(wc, interpolation="bilinear")
    ax2.axis("off")
    st.pyplot(fig2)

st.subheader("Average stipend by city")
stipend_city = filtered.groupby("location")["stipend_clean"].mean().dropna().sort_values(ascending=False).head(10)
fig3, ax3 = plt.subplots(figsize=(8,5))
ax3.barh(stipend_city.index, stipend_city.values, color="salmon")
ax3.set_xlabel("Avg Stipend (₹)")
plt.tight_layout()
st.pyplot(fig3)