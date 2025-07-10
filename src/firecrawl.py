import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("API Key for firecrawl does not exist")
        self.app = FirecrawlApp(api_key=api_key)
    
    def search_for_rules(self, query: str, num_results: int = 3):
        """Searches the web to get info on how to play particular endgames given the different pieces"""
        try:
            result = self.app.search(query = query, limit=num_results, scrape_options= ScrapeOptions(
                formats = ['markdown']
            ))
            return result
        except Exception as e:
            print(e)
            return []
        
    def scrape_websites(self, url: str):
        """Searches the websites found from the previous function and scrapes each web"""
        try:
            result = self.app.scrape_url(url, formats= ['markdown'])
            return result
        except Exception as e:
            print(e)
            return []
        