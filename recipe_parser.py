import cloudscraper
import re
from bs4 import BeautifulSoup
from bs4.element import Tag


class RecipeParser:
    def __init__(self, url):
        self.ingredients_regex = re.compile(".*ingredients*")
        self.directions_regex = re.compile(".*instruction*|.*direction*|.*method*")

        # Init BeautifulSoup
        formatted_url = self.format_url(url)
        self.soup = self.setup_soup(formatted_url)

    def format_url(self, url):
        if url.startswith("http://"):
            prefix = "http://"
        elif url.startswith("https://"):
            prefix = "https://"
        else:
            prefix = ""

        formatted_url = "http://" + url[len(prefix):]
        return formatted_url

    def setup_soup(self, url):
        # Scrape the given url while bypassing cloudflare bot prevention
        scraper = cloudscraper.create_scraper()
        page = scraper.get(url)
        return BeautifulSoup(page.content, "html.parser")

    def parse_section(self, regex):
        list_container = self.soup.find(["ul", "ol"], class_=regex)

        # Recursively get the string representation of the children
        # Only get the text of Tags since .children might also return NavigableString
        list_items = [
            i.get_text() for i in list_container.children if type(i) == Tag
        ]

        # Remove the empty and whitespace strings from the list
        list_items = list(map(str.strip, filter(str.strip, list_items)))

        # TODO: Might not be needed in order to look nice in app
        # Replace all the thin space unicode characters with a normal space
        list_items = list(map(lambda i: i.replace("\u2009", " "), list_items))
        return list_items

    def get_ingredients(self):
        return self.parse_section(self.ingredients_regex)

    def get_directions(self):
        return self.parse_section(self.directions_regex)


if __name__ == "__main__":
    url = input("URL: ")
    parser = RecipeParser(url)
    print("INGREDIENTS:\n", parser.get_ingredients())
    print("DIRECTIONS:\n", parser.get_directions())

