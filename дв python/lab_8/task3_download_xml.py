"""
Завантаження XML-файлу — задача 3
- Приклад завантаження XML, збереження і первинного аналізу.
- Обробка помилок, трасування.
"""

import requests
import time
import os
import sys
import xml.etree.ElementTree as ET

DEFAULT_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
OUTFILE = "ecb_rates.xml"

def download_xml(url=DEFAULT_URL, outfile=OUTFILE, retries=3, delay=10):
    attempt = 0
    while attempt < retries:
        attempt += 1
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Спроба {attempt} завантажити XML: {url}")
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; xml-download/1.0)"}
            r = requests.get(url, headers=headers, timeout=15)
            print(f"  HTTP {r.status_code}, Content-Type: {r.headers.get('content-type')}")
            r.raise_for_status()
            with open(outfile, "wb") as f:
                f.write(r.content)
            print(f"  Файл збережено: {os.path.abspath(outfile)} (байт: {len(r.content)})")
            return outfile
        except requests.RequestException as e:
            print("  Помилка:", e)
            if attempt < retries:
                print(f"  Чекаю {delay} сек перед повтором...")
                time.sleep(delay)
            else:
                print("  Максимум спроб вичерпано.")
                raise

def quick_parse_and_inspect(xmlfile):
    print(f"  Починаю парсинг: {xmlfile}")
    try:
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        print("  Кореневий тег:", root.tag)
        # Для ECB — глибше: знайдемо елементи Cube з атрибутами time і currency/rate
        cubes = root.findall(".//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube")
        # Якщо простір імен не дозволяє знайти, спробуємо без NS
        if not cubes:
            cubes = root.findall(".//Cube")
        print(f"  Знайдено {len(cubes)} елементів 'Cube' (можливо включаючи вкладені)")
        # Вибрати набори з атрибутом time
        times = root.findall(".//Cube[@time]")
        if times:
            for t in times:
                date = t.attrib.get("time")
                print(f"  Дата курсу: {date}, кількість валют у цьому блоку: {len(t)}")
                # покажемо перші 5 валют
                for i, c in enumerate(list(t)[:5]):
                    print(f"    {i+1}. {c.attrib.get('currency')} = {c.attrib.get('rate')}")
        else:
            print("  Не знайдено блоків з атрибутом 'time' (можливо інший формат XML).")
    except ET.ParseError as e:
        print("  Помилка парсингу XML:", e)
        raise

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    out = sys.argv[2] if len(sys.argv) > 2 else OUTFILE
    try:
        fn = download_xml(url, out)
        quick_parse_and_inspect(fn)
    except Exception as e:
        print("Сценарій завершився помилкою:", e)