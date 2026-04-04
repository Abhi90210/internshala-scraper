# InternIQ — Internshala Skills Analyser

A web scraping + data analysis app that scrapes real internship listings from Internshala and reveals what skills companies actually want.

🔗 **Live Demo**: [https://internshala-scraper-7upml4er6aossqcqxc7kxr.streamlit.app/](https://internshala-scraper-7upml4er6aossqcqxc7kxr.streamlit.app/)
📂 **GitHub**: [https://github.com/Abhi90210/internshala-scraper](https://github.com/Abhi90210/internshala-scraper)

> Demo login — Username: `admin` | Password: `intern123`

---

## What it does

- Scrapes 400+ real internship listings from Internshala using `requests` and `BeautifulSoup`
- Extracts job title, company, location, stipend, and required skills from each listing
- Analyses the most in-demand skills, top hiring cities, and average stipends
- Displays everything in an interactive Streamlit dashboard with live filters

---

## Features

- **Login system** — username/password authentication with session state
- **Dashboard** — metric cards, top locations, stipend by city, top companies
- **Skills Analysis** — top 20 skills bar chart + skills word cloud + skill tags
- **Data Explorer** — searchable, filterable table of all listings
- **Feedback page** — users can rate and review the app
- **Animated UI** — smooth fade-in animations, hover effects, modern theme

---

## Tech stack

| Tool | Purpose |
|------|---------|
| `requests` | Fetch Internshala web pages |
| `BeautifulSoup` | Parse HTML and extract data |
| `pandas` | Clean and analyse scraped data |
| `matplotlib` | Charts and visualisations |
| `wordcloud` | Skills word cloud |
| `Streamlit` | Interactive web dashboard |
| `Streamlit Cloud` | Free deployment |

---

## How to run locally

```bash
# 1. Clone the repo
git clone https://github.com/Abhi90210/internshala-scraper.git
cd internshala-scraper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Scrape fresh data
python scraper.py

# 4. Run the app
streamlit run app.py
```

---

## Project structure

```
internshala-scraper/
├── app.py              # Streamlit dashboard
├── scraper.py          # Internshala web scraper
├── internships.csv     # Scraped dataset
├── feedback.csv        # User feedback (auto-generated)
├── requirements.txt    # Dependencies
└── README.md
```

---

## Key findings from the data

- Most internships are concentrated in Bangalore, Mumbai, Delhi and Remote
- Top skills in demand: Excel, Communication, Python, Social Media, MS Office
- Remote internships offer competitive stipends compared to metro cities

---

## What I learned

- How to inspect HTML structure using browser DevTools to identify scraping targets
- Real-world data is messy — stipends come in formats like "₹10,000 - 15,000 /month" requiring custom cleaning
- Adding random delays between requests prevents getting blocked by the server
- BeautifulSoup + requests is a powerful combo for any structured website

---

*Built by Abhi90210 — 2nd year Electronics and Computer Science student, Pune*