import requests
import json
from bs4 import BeautifulSoup

class Tag:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Tag(name='{self.name}')"

def get_author_info(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def parse_data():    
    url = 'http://quotes.toscrape.com/'
    next_page = "/page/1/"
    authors_data = {}
    quotes_data = []

    while next_page:
        response = requests.get(url + next_page)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            quote_text = quote.find('span', class_='text').text.strip()
            author_name = quote.find('small', class_='author').text.strip()
            tags = [Tag(name=tag.text.strip()) for tag in quote.find_all('a', class_='tag')]

            if author_name not in authors_data:
                author_url = quote.find('a')['href']
                author_info = get_author_info(url + author_url)
                authors_data[author_name] = author_info

            quote_data = {
                "tags": tags,
                "author": authors_data[author_name]['fullname'],
                "quote": quote_text                
            }
            quotes_data.append(quote_data)

        next_page_tag = soup.find('li', class_='next')
        next_page = next_page_tag.find('a')['href'] if next_page_tag else None

    return authors_data, quotes_data


def save_to_json(authors_data, quotes_data):
    authors_list = list(authors_data.values())
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_list, f, ensure_ascii=False, indent=4)
    
    quotes_list = []
    for quote_data in quotes_data:
        quotes_list.append({
            "tags": [tag.name for tag in quote_data["tags"]],
            "author": quote_data["author"],
            "quote": quote_data["quote"]            
        })

    with open('qoutes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes_list, f, ensure_ascii=False, indent=4)


def main():
    authors_data, quotes_data = parse_data()
    save_to_json(authors_data, quotes_data)

if __name__ == "__main__":
    main()    