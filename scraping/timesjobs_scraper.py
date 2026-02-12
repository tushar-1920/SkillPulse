# timesjobs_scraper.py
import csv
from bs4 import BeautifulSoup
from base_scraper import BaseScraper



class TimesJobsScraper(BaseScraper):

    def fetch_jobs(self, keyword, location, pages=1):

        all_jobs = []

        keyword = keyword.replace(" ", "+")
        location = location.replace(" ", "+")

        for page in range(1, pages + 1):

            url = (
                "https://www.timesjobs.com/candidate/job-search.html"
                f"?searchType=personalizedSearch&from=submit"
                f"&txtKeywords={keyword}"
                f"&txtLocation={location}"
                f"&sequence={page}"
            )

            print(f"Scraping: {url}")

            html = self.get(url)
            soup = BeautifulSoup(html, "html.parser")

            job_cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

            for job in job_cards:
                title = self._get_text(job, "h2")
                company = self._get_company(job)
                location = self._get_location(job)
                description = self._get_description(job)
                url = self._get_url(job)

                all_jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "url": url
                })

        return all_jobs

    def _get_text(self, job, tag):
        t = job.find(tag)
        if t:
            return t.get_text(strip=True)
        return ""

    def _get_company(self, job):
        c = job.find("h3", class_="joblist-comp-name")
        if c:
            return c.get_text(strip=True)
        return ""

    def _get_location(self, job):
        span = job.find("span", class_="sim-posted")
        if span:
            return span.get_text(strip=True)
        return ""

    def _get_description(self, job):
        ul = job.find("ul", class_="list-job-dtl")
        if ul:
            return ul.get_text(" ", strip=True)
        return ""

    def _get_url(self, job):
        h2 = job.find("h2")
        if not h2:
            return ""

        a = h2.find("a")
        if a and a.has_attr("href"):
            return a["href"]
        return ""


def save_to_csv(jobs, path):
    if not jobs:
        print("No jobs found.")
        return

    keys = jobs[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} jobs to {path}")


if __name__ == "__main__":
    scraper = TimesJobsScraper()

    jobs = scraper.fetch_jobs(
        keyword="data scientist",
        location="Bangalore",
        pages=2
    )

    save_to_csv(jobs, "data/raw_jobs.csv")
