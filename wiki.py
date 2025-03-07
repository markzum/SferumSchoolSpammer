import requests
from bs4 import BeautifulSoup

def get_image(object_name: str) -> str:
    host = "https://ru.wikipedia.org"

    search_url = f"{host}/w/index.php?search={object_name.replace(' ', '+')}"
    search_response = requests.get(search_url)
    if search_response.status_code != 200:
        return "Ошибка при доступе к Википедии"
    
    if search_response.status_code != 200:
        return "Страница не найдена"
    
    try:
        soup = BeautifulSoup(search_response.text, 'html.parser')
        try:
            link = soup.find("table", class_="infobox").find("a", class_="mw-file-description")["href"]
        except:
            page = soup.find("div", class_="mw-body-content").find("a")["href"]
            page_response = requests.get(f"{host}{page}")
            soup = BeautifulSoup(page_response.text, 'html.parser')
            link = soup.find("table", class_="infobox").find("a", class_="mw-file-description")["href"]

        link = f"{host}{link}"
        image_response = requests.get(link)
        
        soup = BeautifulSoup(image_response.text, 'html.parser')
        image_link = soup.find("a", class_="internal")["href"]

        return f"https:{image_link}"
    except Exception as e:
        # print(e)
        return None


if __name__ == "__main__":
    print(get_image("Гиббон"))
