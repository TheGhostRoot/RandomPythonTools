import requests
from bs4 import BeautifulSoup

# Get the topic of the essay from the user
topic = input("Enter the topic of the essay: ")
fileName = input("Enter the file name with the format: ")

# Use the requests library to fetch the webpage for the topic
page = requests.get(f"https://en.wikipedia.org/wiki/{topic}")

# Use BeautifulSoup to parse the HTML of the webpage
soup = BeautifulSoup(page.content, 'html.parser')

# Find all the paragraphs on the page
paragraphs = soup.find_all('p')
file = open(fileName, 'a')
# Iterate over the paragraphs
for p in paragraphs:
    # Remove any <sup> elements from the paragraph (these contain citations)
    for sup in p.find_all('sup'):
        sup.decompose()
    # Print the text of the paragraph
    print(p.text)
    file.write(p.text+'\n')
    file.close()
