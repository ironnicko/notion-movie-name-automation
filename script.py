from collections import deque
import requests
from os import getenv
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


token = getenv("TOKEN_ID")
database_id = getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

base_url = "https://api.notion.com/v1"


def get_database(database_id):

    req_url = f"{base_url}/databases/{database_id}/query"

    response = requests.post(req_url, headers=headers)

    data = response.json()

    if response.status_code == 200:
        return data
    else:
        print(f"Error: {response.status_code}")
        return None


def update_url(page_id, url):
    req_url = f"{base_url}/pages/{page_id}"
    data = {"properties": {
        "Link": {
            "url": url
        }
    }}
    print(data)
    response = requests.patch(req_url, headers=headers, json=data)


def process_data(json):
    results = json["results"]
    for res in results:
        property = res["properties"]
        page_id = res["id"]
        name = property["Name"]["title"][0]["text"]["content"]
        url = property["Link"]["url"]
        if not url:
            links = [get_link(name, "netflix"), get_link(
                name, "primevideo")]
            add = 0
            for link in links:
                add += link[0]
            links = deque(links)
            if add == 0:
                continue
            while links[0][0] == 0:
                links.popleft()
            url = links[0][1]

            # print(netflix_url)
            update_url(page_id, url)


def get_link(name, platform):
    req_url = f"https://www.google.com/search?q={
        '+'.join(name.split())}+{platform}"

    respsone = requests.get(req_url)

    soup = BeautifulSoup(respsone.content, "html.parser")

    link = ""

    check_link = [f"https://www.{platform}.com/title",
                  f"https://www.{platform}.com/detail"]

    if platform == "netflix":
        check_link = check_link[0]
    elif platform == "primevideo":
        check_link = check_link[1]

    for link in soup.find_all('a'):
        link = link.get("href")
        if check_link in link:
            index = link.find("&")
            link = link[:index].strip("/url?q=")
            break

    return (check_link in link), link


print("Starting...")

if __name__ == '__main__':
    data = get_database(database_id)
    if data:
        process_data(data)
    else:
        print("Failed to fetch the database, please add your integration as connection in your notion database.")
