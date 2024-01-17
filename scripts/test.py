import glob
from bs4 import BeautifulSoup
import requests

def find_unresolved_attributes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return body_content.find_all(text=lambda t: "{" in t and "}" in t)
    else:
        return []


def find_broken_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    broken_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            try:
                response = requests.head(href, allow_redirects=True, timeout=5)
                if response.status_code != 200:
                    broken_links.append(href)
            except requests.RequestException:
                broken_links.append(href)
        # Add more conditions for other types of links if necessary
    return broken_links

def check_unique_ids(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    ids = [element['id'] for element in soup.find_all(id=True)]
    return len(ids) != len(set(ids))

# Main script logic
html_files = glob.glob('./build/*/*.html')  # Adjust the path as needed
for file in html_files:
    with open(file, 'r') as f:
        content = f.read()
        unresolved = find_unresolved_attributes(content)
        broken_links = find_broken_links(content)
        non_unique_ids = check_unique_ids(content)

        # Report findings
        print(f"File: {file}")
        print(f"Unresolved Attributes: {unresolved}")
        print(f"Broken Links: {broken_links}")
        print(f"Non-Unique IDs: {non_unique_ids}")
