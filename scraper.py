from bs4 import BeautifulSoup
import requests
    

def scrape(url):

    """Given a URL, fetch the page and return clean, readable text — stripped of HTML tags, scripts, nav bars, ads, etc.
      This is the raw material everything else in our pipeline depends on"""
    
    response = requests.get(url, timeout=10)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(f"Failed to retrieve webpage: {error}") from error
    
    soup = BeautifulSoup(response.content, "html.parser")       # Parse the HTML content using BeautifulSoup

    # Stripping junk tags
    for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script.extract()                # Remove these tags from the soup
    clean_text = soup.get_text(separator="\n", strip=True)

    if not clean_text:
        raise ValueError("The webpage contains no readable text.")

    return clean_text    # Return the cleaned text, stripped of leading/trailing whitespace


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        text = scrape(url)
        print(text[:500])  # Print the first 500 characters of the scraped text
    except ValueError as e:
        print(e)