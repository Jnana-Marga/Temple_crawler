from urllib.robotparser import RobotFileParser
from duckpy import Client
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
from urllib.error import URLError

def is_crawling_allowed(url):
    try:
        rp = RobotFileParser()
        robots_url = f"{url.rstrip('/')}/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except URLError as e:
        print(f"Error while fetching robots.txt(robots.txt file doesnot exist for this website)")
        return True

def crawl(url, limit):
    try: 
        if limit <= 0:
            return

        if not is_crawling_allowed(url):
            print(f"Crawling not allowed for {url}")
            return

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = soup.find_all('p')
        for p in paragraphs:
            cleaned_text = p.text.strip()
            if not cleaned_text or cleaned_text.isspace():
                continue
            pattern = r'[\t]{2,}|@'
            match = re.search(pattern, cleaned_text)
            if match:
                continue
            else:  
                print(cleaned_text)

        images = soup.find_all('img')
        for image in images:
            src = image.get('src')
            print("Image URL: ", src)

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href is not None:
                if href.startswith('https://'):
                        #print("Absolute Link: ",href)
                        crawl(href, limit - 1)
                else:
                    absolute_link = urljoin(url,href)
                    if absolute_link.startswith(("https://","http://")):
                            crawl(absolute_link,limit-1)
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

q = input("Enter Temple name: ")
client = Client()
results = client.search(q + "official website")
for i in range(0, 5):
    li = results[i].url
    print("\nWebsite Url: ", li, "\n")
    crawl(li, 3)
