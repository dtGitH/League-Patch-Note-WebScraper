import requests
from bs4 import BeautifulSoup

# URL of the LoL patch notes page
url = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-1-notes/'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the h4 tags with class 'change-detail-title'
change_categories = soup.find_all('h4', class_='change-detail-title')

# Initialize a dictionary to hold the data
patch_data = {}

# Loop through each change category and extract the relevant data
for category in change_categories:
    # The category name is the text of the h4 tag
    category_name = category.get_text().strip()

    # Skip sections you don't need (e.g., "Bugfixes")
    if category_name.lower() == 'bugfixes':
        break  # This will exit the loop and ignore all sections after "Bugfixes"

    patch_data[category_name] = []

    # The first strong tag after the h4 tag contains the subject of the change
    next_element = category.find_next()
    while next_element and next_element.name != 'h4':
        if next_element.name == 'strong':
            subject_name = next_element.get_text().strip()
            details_list = next_element.find_next('ul')
            details = [detail.get_text().strip() for detail in details_list.find_all('li')] if details_list else []
            patch_data[category_name].append({'subject': subject_name, 'details': details})
        next_element = next_element.find_next()

# Print the extracted data
for category, subjects in patch_data.items():
    print(f"{category}:")
    for subject in subjects:
        print(f" - Subject: {subject['subject']}")
        for detail in subject['details']:
            print(f"   Detail: {detail}")
        print("\n")
    print("\n")
