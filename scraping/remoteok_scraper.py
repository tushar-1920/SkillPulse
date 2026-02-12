import csv
import requests


class RemoteOKScraper:

    def fetch_jobs(self, keyword="data", limit=50):

        url = "https://remoteok.com/api"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()

        data = resp.json()

        jobs = []

        for item in data[1:]:
            if keyword.lower() in item.get("position", "").lower():
                jobs.append({
                    "title": item.get("position", ""),
                    "company": item.get("company", ""),
                    "location": item.get("location", ""),
                    "description": item.get("description", ""),
                    "url": item.get("url", "")
                })

            if len(jobs) >= limit:
                break

        return jobs


def save_to_csv(jobs, path):
    if not jobs:
        print("No jobs found")
        return

    keys = jobs[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)


if __name__ == "__main__":
    scraper = RemoteOKScraper()
    jobs = scraper.fetch_jobs(keyword="data", limit=100)
    save_to_csv(jobs, "data/raw_jobs.csv")
    print("Saved jobs:", len(jobs))
