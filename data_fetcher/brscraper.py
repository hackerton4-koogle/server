import requests
from bs4 import BeautifulSoup

class BlueRibbonSurveryScraper:
    def scrape(self):
        base_url = "https://www.bluer.co.kr/api/v1/restaurants?page={}&size=30&query=&foodType=&foodTypeDetail=&feature=&location=&locationDetail=&area=&areaDetail=&priceRange=&ribbonType=&recommended=false&isSearchName=false&tabMode=single&searchMode=map&zone1=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%B6%81&zone2=%ED%99%8D%EB%8C%80%EC%95%9E%2F%EC%84%9C%EA%B5%90%EB%8F%99&zone2Lat=37.553335937996756&zone2Lng=126.92488217617958"

        restaurant_list = []
        page = 0

        while True:
            response = requests.get(base_url.format(page))
            if response.status_code == 200:
                data = response.json()
                if not data["_embedded"]["restaurants"]:
                    break

                for restaurant_data in data["_embedded"]["restaurants"]:
                    restaurant = {
                        "name": restaurant_data["headerInfo"]["nameKR"],
                        "phone": restaurant_data["defaultInfo"]["phone"],
                        "description": restaurant_data["review"]["review"],
                        "image_url": f"https://www.bluer.co.kr{restaurant_data['firstImage']['url']}"
                    }
                    restaurant_list.append(restaurant)

                page += 1
            else:
                print("Failed to fetch data.")
                break

        return restaurant_list

scraper = BlueRibbonSurveryScraper()
restaurant_list = scraper.scrape()

for restaurant in restaurant_list:
    print(restaurant)
