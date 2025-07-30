
import requests
from bs4 import BeautifulSoup
import csv
import sys

PAGE_URL = "https://junglegenius.deno.dev/vontive/3"
API_ENDPOINT = "https://junglegenius.deno.dev/vontive/getEngineer"

def fetch_page(url):
    resp = requests.get(url)
    resp.raise_for_status()

    with open("../retrievedsite.html", "w", encoding="utf-8") as html_file:
        html_file.write(resp.text)
    
    with open("retrievedsite.html", "w", encoding="utf-8") as html_file:
        html_file.write(resp.text)

    return resp.text

def extract_ids(html):
    soup = BeautifulSoup(html, "html.parser")
    details = soup.select("details.engineer-section")
    ids = []
    for d in details:
        id_attr = d.get("data-engineer-id")
        if id_attr:
            ids.append(id_attr)
    return ids

def fetch_engineer(id_):
    params = {"id": id_}
    r = requests.get(API_ENDPOINT, params=params)
    r.raise_for_status()
    return r.json()

def save_csv(engineers, fn="engineers.csv"):
    with open(fn, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name",
            "jobTitle",
            "education",
            "yearsAtVontive",
            "experience",
        ])
        for e in engineers:
            writer.writerow([

                e.get("firstName", "") + " " + e.get("lastName", ""),
                e.get("jobTitle", ""),
                ";".join(e.get("education", [])),
                e.get("yearsAtVontive", ""),
                ";".join(e.get("experience", [])),
            ])

def main():
    try:
        html = fetch_page(PAGE_URL)
    except Exception as e:
        print("Error fetching page:", e, file=sys.stderr)
        sys.exit(1)

    ids = extract_ids(html)
    if not ids:
        print("No engineer IDs found on page.", file=sys.stderr)
        sys.exit(1)

    engineers = []
    for id_ in ids:
        try:
            eng = fetch_engineer(id_)
            engineers.append(eng)
        except Exception as e:
            print(f"Error fetching engineer {id_}:", e, file=sys.stderr)

    if not engineers:
        print("No engineer data retrieved.", file=sys.stderr)
        sys.exit(1)

    save_csv(engineers)
    print(f"Done: scraped {len(engineers)} engineers → engineers.csv")

if __name__ == "__main__":
    main()
