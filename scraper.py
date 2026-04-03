import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    
    internships = []
    cards = soup.find_all("div", class_="internship_meta")
    
    for card in cards:
        try:
            title = card.find("a", class_="job-title-href").text.strip()
        except:
            title = "N/A"
        
        try:
            company = card.find("p", class_="company-name").text.strip()
        except:
            company = "N/A"
        
        try:
            location = card.find("div", class_="locations").find("a").text.strip()
        except:
            location = "N/A"
        
        try:
            stipend = card.find("span", class_="stipend").text.strip()
        except:
            stipend = "N/A"

        try:
            skills = card.find_all("div", class_="job_skill")
            skills_list = ", ".join([s.text.strip() for s in skills])
        except:
            skills_list = "N/A"
        
        internships.append({
            "title": title,
            "company": company,
            "location": location,
            "stipend": stipend,
            "skills": skills_list
        })
    
    return internships

all_data = []

for page in range(1, 11):
    url = f"https://internshala.com/internships/page-{page}"
    print(f"Scraping page {page}...")
    data = scrape_page(url)
    all_data.extend(data)
    time.sleep(random.uniform(2, 4))

df = pd.DataFrame(all_data)
df.to_csv("internships.csv", index=False)
print(f"Done! Scraped {len(df)} internships.")
print(df.head())