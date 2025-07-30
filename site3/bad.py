
import requests
from bs4 import BeautifulSoup
import csv

PAGE_URL = "https://junglegenius.deno.dev/vontive/3"

def scrape_engineers(url):
    resp = requests.get(url)
    resp.raise_for_status()

    with open("../retrievedsite.html", "w", encoding="utf-8") as html_file:
        html_file.write(resp.text)
    
    with open("retrievedsite.html", "w", encoding="utf-8") as html_file:
        html_file.write(resp.text)

    soup = BeautifulSoup(resp.text, "html.parser")

    engineers = []
    for det in soup.select("details.engineer-section"):

        name = det.select_one("summary.engineer-name").get_text(strip=True)


        years = det.select_one("span.engineer-years-value").get_text(strip=True)


        education = [
            li.get_text(strip=True)
            for li in det.select("ul.engineer-education-list li.engineer-education-item")
        ]


        experience = [
            li.get_text(strip=True)
            for li in det.select("ul.engineer-experience-list li.engineer-experience-item")
        ]

        engineers.append({
            "Name": name,
            "YearsAtVontive": years,
            "Education": education,
            "Experience": experience,
        })

    return engineers

def save_to_csv(engineers, filename="engineers.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["Name", "YearsAtVontive", "Education", "Experience"])

        for e in engineers:
            writer.writerow([
                e["Name"],
                e["YearsAtVontive"],
                ";".join(e["Education"]),
                ";".join(e["Experience"]),
            ])

if __name__ == "__main__":

    engineers = scrape_engineers(PAGE_URL)
    save_to_csv(engineers)
    print(f"Scraped {len(engineers)} engineers, wrote engineers.csv, and saved retrievedsite.html")
