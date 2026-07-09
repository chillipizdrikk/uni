import threading
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

class Scraper(threading.Thread):
    def __init__(self, url, name):
        super().__init__()
        self.url = url
        self.name = name

    def run(self):
        print(f"Сайт {self.name}:")
        response = urlopen(self.url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    
        elements = ['div.s_price__W9J5t', 'div.t-cell.bold.size18', 'div.text-price-bp']
        for element in elements:
            data = soup.select_one(element)
            if data is not None:
                print(f"Ціна пального А-95: {data.text} грн")

        total_time = 0
        for i in range(5):
            start_time = time.time()
            response = urlopen(self.url)
            end_time = time.time()
            total_time += end_time - start_time
            print(f"Час виконання запиту {i+1}: {format(end_time - start_time, '.5f')} секунд")

        end_time = time.time()
        print(f"Середній час виконання запиту на сайті {self.name}: {format((total_time) / 5, '.5f')} секунд\n")

urls = ['https://wog.ua/ua/fuels/', 
        'https://auto.ria.com/uk/toplivo/', 
        'https://olas.com.ua/index.php?route=information/information&information_id=9']

for i, url in enumerate(urls):
    scraper = Scraper(url, f"{i+1}")
    scraper.start()
    scraper.join()





# import urllib.request
# from bs4 import BeautifulSoup
# import time
# import threading

# def get_fuel_price(url, html_element):
#     with urllib.request.urlopen(url) as response:
#         html = response.read()
#     soup = BeautifulSoup(html, 'html.parser')
#     data = soup.select_one(html_element)
#     print(f"Ціна А-95 з цього сайту\n{url}: {data.get_text() if data else 'No data found'} грн\n")


# urls = ['https://wog.ua/ua/fuels/', 'https://auto.ria.com/uk/toplivo/', 'https://olas.com.ua/index.php?route=information/information&information_id=9']
# html_elements = ['div.s_price__W9J5t', 'div.t-cell.bold.size18', 'div.text-price-bp'] 
# for iteration in range(1, 6):
#     print(f"\nВиконання {iteration}:\n")
#     start = time.time()
#     threads = []

#     for i in range(len(urls)):
#         thread = threading.Thread(target=get_fuel_price, args=(urls[i], html_elements[i]))
#         thread.start()
#         threads.append(thread)

#     for thread in threads:
#         thread.join()

#     end = time.time()
#     print('Середній час виконання: ', end - start)