import requests
import certifi
from abc import ABC, abstractmethod


class BaseScraper(ABC):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def get(self, url):

        try:
            response = requests.get(
            url,
            headers=self.headers,
            timeout=20,
            verify=certifi.where()
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.SSLError as e:
            print("SSL error while accessing:", url)
            raise e


    @abstractmethod
    def fetch_jobs(self, keyword, location, pages=1):
        pass
