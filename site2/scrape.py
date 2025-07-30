
import requests
from bs4 import BeautifulSoup
import csv
import json

PAGE_URL = "https://junglegenius.deno.dev/vontive/2"

def scrape_engineers(url):

    resp = requests.get(url)
    resp.raise_for_status()

    with open("retrievedsite.html", "w", encoding="utf-8") as f_html:
        f_html.write(resp.text)

    soup = BeautifulSoup(resp.text, "html.parser")
    script = soup.find("script", {"id": "initial-data", "type": "application/json"})
    if not script or not script.string:
        raise RuntimeError("Could not find <script id='initial-data'> with JSON payload")

    engineers = json.loads(script.string)

    return engineers


def save_to_csv(engineers, filename="engineers.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv)

        writer.writerow([
            "Name",
            "jobTitle",
            "education",
            "yearsAtVontive",
            "experience",
        ])

        for e in engineers:
            writer.writerow([
                e.get("firstName") +" "+e.get("lastName"),
                e.get("jobTitle"),
                ";".join(e.get("education", [])),
                e.get("yearsAtVontive"),
                ";".join(e.get("experience", [])),
            ])

if __name__ == "__main__":

    engineers = scrape_engineers(PAGE_URL)
    save_to_csv(engineers)

    print(f"Scraped {len(engineers)} engineers, wrote engineers.csv, and saved retrievedsite.html")
