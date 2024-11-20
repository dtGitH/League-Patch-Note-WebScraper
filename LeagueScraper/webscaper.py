import requests
from bs4 import BeautifulSoup


class PatchNotesScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.patch_data = {}

    def fetch_page(self):
        """Fetch the HTML content of the webpage."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            self.soup = None

    def parse_patch_notes(self):
        """Parse the patch notes from the HTML content."""
        if not self.soup:
            return

        # Locate the container for patch notes
        patch_notes_container = self.soup.find('div', id='patch-notes-container')
        if not patch_notes_container:
            print("Error: Patch notes container not found.")
            return

        # Find all categories (h4 elements)
        categories = patch_notes_container.find_all('h4', class_='change-detail-title')

        for category in categories:
            category_name = category.get_text(strip=True)
            if category_name not in self.patch_data:
                self.patch_data[category_name] = []

            # Stop processing after "Item Nerfs"
            if category_name == "Item Nerfs":
                self.patch_data[category_name] = self.parse_category_items(category)
                break

            # Parse other categories normally
            self.patch_data[category_name] = self.parse_category_items(category)

    def parse_category_items(self, category):
        """Parse items and details for a given category."""
        items = []
        next_element = category.find_next_sibling()
        while next_element:
            if next_element.name == 'strong':  # Subject header
                subject_name = next_element.get_text(strip=True)
                details_list = next_element.find_next('ul')  # Find the following <ul> for details
                details = (
                    [detail.get_text(strip=True) for detail in details_list.find_all('li')]
                    if details_list
                    else []
                )
                # Skip empty or malformed data
                if subject_name and details:
                    description = " ".join(details)
                    items.append({'item': subject_name, 'description': description})
            next_element = next_element.find_next_sibling()  # Move to the next sibling
        return items

    def display_patch_notes(self):
        """Display the parsed patch notes."""
        if not self.patch_data:
            print("No patch notes available.")
            return

        for category, items in self.patch_data.items():
            print(f"{category}:")
            for item in items:
                print(f"{item['item']}: ({item['description']})")
            print("\n")


# Usage
if __name__ == "__main__":
    url = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-1-notes/'
    scraper = PatchNotesScraper(url)
    scraper.fetch_page()
    scraper.parse_patch_notes()
    scraper.display_patch_notes()
