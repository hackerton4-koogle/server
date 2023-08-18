import requests
from bs4 import BeautifulSoup
import re

class BlueRibbonSurveryScraper:
    def scrape(self):
        base_url = "https://www.bluer.co.kr/api/v1/restaurants?page={}&size=30&query=&foodType=&foodTypeDetail=&feature=&location=&locationDetail=&area=&areaDetail=&priceRange=&ribbonType=&recommended=false&isSearchName=false&tabMode=single&searchMode=map&zone1=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%B6%81&zone2=%ED%99%8D%EB%8C%80%EC%95%9E%2F%EC%84%9C%EA%B5%90%EB%8F%99&zone2Lat=37.553335937996756&zone2Lng=126.92488217617958"

        restaurant_list = []
        page = 0

        while True:
            response = requests.get(base_url.format(page))
            if response.status_code == 200:
                data = response.json()

                try:
                    data["_embedded"]["restaurants"]
                except KeyError:
                    return restaurant_list

                for restaurant_data in data["_embedded"]["restaurants"]:
                    restaurant = {
                        "name": restaurant_data["headerInfo"]["nameKR"],
                        "phone": restaurant_data["defaultInfo"]["phone"],
                        "description": restaurant_data["review"]["review"],
                        # "image_url": f"https://www.bluer.co.kr{restaurant_data['firstImage']['url']}"
                    }
                    restaurant_list.append(restaurant)
                

                page += 1
            else:
                print("Failed to fetch data.")
                break

        return restaurant_list

class TasteOfSeoulScraper:
    def scrape_page(self, base_url, page):
        res = []
        
        places = page.find('ul', class_='listType1').find_all('li')
        for place in places:
            category = place.find(class_='cate').text
            
            image_attr = place.find(class_='imgBox')['style']
            pattern = re.compile(r'url\(/(.*?)\)')
            image_url = pattern.search(image_attr).group(1)
            image_url = base_url + image_url

            name = place.find('dt').text
            phone = place.find(class_='tel').text
            
            description = place.find('dd').text

            res.append({'category': category, 
                        'name': name, 
                        'phone': phone, 
                        'image_url': image_url,
                        'description': description, 
                        })
            
        return res

    def scrape(self):
        params = {
            'page': 1
        }
        base_url = 'https://tasteofseoul.visitseoul.net/'
        url = base_url + '_subpage/kor/restaurants/list.php'

        
        

        res = []

        retries = 0
        while(True):
            try: 
                response = requests.get(url, params, timeout=5)
                response.raise_for_status()
            except requests.Timeout as e:
                print(f'Timeout on {response.url}')
                if retries == 3:
                    print(f'Stop: {retries} retries on {response.url}')
                    return
                retries = retries + 1
                print(f'Retrying({retries})')
                continue
            except requests.TooManyRedirects as e:
                print(f'Stop: Too many redirects on {response.url}')
                print(str(e))
                return
            except requests.exceptions.RequestException as e:
                print(f'Stop: Exception on {response.url}')
                print(str(e))
                return

            page = BeautifulSoup(response.content, 'html.parser')
            places = self.scrape_page(base_url, page)
            res += places

            exists_next_page = page.find('a', class_='last')
            if not exists_next_page: break
            
            retries = 0
            params = {
                'page': params['page'] + 1
            }

        return res
    


if __name__ == '__main__':
    lst = TasteOfSeoulScraper().scrape()
    for place in lst:
        for key in place:
            print(f'{key:<16} {place[key]}')
        print('')
    
    