Please Install these packages using:-
pip install urllib3
pip install beautifulsoup4
pip install requests
pip install duckpy

Here's the documentation for the code:

Imported Libraries:

urllib.robotparser: Library for parsing robots.txt files to check crawling permissions.
duckpy.Client: DuckDuckGo Instant Answer API client to search for relevant websites.
requests: HTTP library for Python to send HTTP requests.
bs4.BeautifulSoup: Library for parsing HTML and extracting data.
json: Python built-in library for working with JSON data.
re: Regular Expression library for pattern matching.
urllib.parse.urljoin: Function to join a base URL and a relative URL to form an absolute URL.
urllib.error.URLError: Exception for URL-related errors.

Function Definitions:

is_crawling_allowed(url):-
 Function to check if crawling is allowed for a given URL based on its robots.txt file. Returns True if crawling is allowed (either the robots.txt file is not found or the URL is allowed according to the robots.txt rules), otherwise returns False.

crawl(url, limit):-
 Recursive function that crawls the website starting from the provided URL up to a specified depth limit. It extracts and prints text paragraphs, image URLs, and hyperlinks from the pages. The depth of crawling is controlled by the limit parameter.


Main Code:

The script prompts the user to enter a "Temple name."
It uses the DuckDuckGo Instant Answer API to search for official websites related to the temple name. The top 5 results are considered.
For each website URL obtained from the search results, the crawl function is called with a depth limit of 3.
The crawl function recursively visits each URL and extracts text paragraphs, image URLs, and hyperlinks.
