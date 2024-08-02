import requests
from bs4 import BeautifulSoup
import json


def get_quotes_from_page(soup):
    quotes = []
    urls = []
    for quote in soup.select('.quote'):
        text = quote.select_one('.text').get_text(strip=True)
        author = quote.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        url = quote.find("a").get("href")
        quotes.append({"quote": text, "author": author, "tags": tags})
        urls.append(url)
    return quotes, urls


def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fullname = soup.select_one('.author-title').get_text(strip=True)
    born_date = soup.select_one('.author-born-date').get_text(strip=True)
    born_location = soup.select_one('.author-born-location').get_text(strip=True)
    description = soup.select_one('.author-description').get_text(strip=True)
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes_and_authors():
    quotes_list = []
    authors_list = []

    base_url = "http://quotes.toscrape.com"
    page_url = "/page/1/"

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.content, 'html.parser')     

        quotes, urls = get_quotes_from_page(soup)
        quotes_list.extend(quotes)

        for url in urls:
            author_url = base_url + url
            author_detail = get_author_details(author_url)
            authors_list.append(author_detail)

        next_page = soup.select_one('.next a')
        page_url = next_page.get('href') if next_page else None

    return quotes_list, authors_list


if __name__ == "__main__":
    quotes, authors = scrape_quotes_and_authors()

    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes, quotes_file, indent=2)

    with open('authors.json', 'w') as authors_file:
        json.dump(authors, authors_file, indent=2)
