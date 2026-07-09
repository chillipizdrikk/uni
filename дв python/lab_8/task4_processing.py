"""
Приклади обробки XML — задача 4
- Декілька незалежних прикладів обробки XML.
- Працює з файлами ECB (курси).
- Демонструє: перебір елементів, пошук за тегом/атрибутом, експорт у CSV, модифікацію і збереження.
"""

import xml.etree.ElementTree as ET
import csv
import os
import sys
from datetime import datetime

def parse_ecb_and_export_csv(xmlfile, csvfile="ecb_rates.csv"):
    print(f"[{datetime.now()}] Парсинг ECB XML: {xmlfile}")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # Спроба знайти блоки з простором імен або без
    # Знайдемо перший елемент Cube з атрибутом time
    times = root.findall(".//Cube[@time]")
    if not times:
        times = root.findall(".//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@time]")
    if not times:
        print("  Не знайдено елементів з атрибутом time. Перевірте формат файлу.")
        return
    # Зазвичай це один блок — останній надрукований
    block = times[0]
    date = block.attrib.get("time")
    print(f"  Дата: {date}  (експортуємо всі валютні курси з цього блоку)")
    rows = []
    for c in block:
        cur = c.attrib.get("currency")
        rate = c.attrib.get("rate")
        rows.append((cur, rate))
    # Додати базову валюту EUR = 1.0
    rows.insert(0, ("EUR", "1.0"))
    with open(csvfile, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["currency", "rate", "date"])
        for cur, rate in rows:
            writer.writerow([cur, rate, date])
    print(f"  Експортовано {len(rows)} рядків у {os.path.abspath(csvfile)}")

def rss_list_items(xmlfile, max_items=10):
    print(f"[{datetime.now()}] Перебір RSS/ATOM: {xmlfile}")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # Спроба знайти item або entry
    items = root.findall(".//item")
    if not items:
        items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    if not items:
        items = root.findall(".//entry")
    print(f"  Знайдено {len(items)} елементів 'item/entry'")
    for i, it in enumerate(items[:max_items]):
        title = it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title")
        link = it.findtext("link") or it.findtext("{http://www.w3.org/2005/Atom}link")
        pub = it.findtext("pubDate") or it.findtext("{http://www.w3.org/2005/Atom}published")
        print(f"  [{i+1}] {title}")
        print(f"       link: {link}")
        print(f"       date: {pub}")

def modify_and_write(xmlfile, outxml="modified.xml"):
    print(f"[{datetime.now()}] Модифікація XML: {xmlfile}")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # Приклад: додати метаінформацію до кореневого елементу
    root.set("processed_by", "task4_processing.py")
    root.set("processed_at", datetime.utcnow().isoformat() + "Z")
    tree.write(outxml, encoding="utf-8", xml_declaration=True)
    print(f"  Модифікований файл збережено у: {os.path.abspath(outxml)}")

def count_nodes(xmlfile):
    print(f"[{datetime.now()}] Підрахунок вузлів у файлі: {xmlfile}")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    count = sum(1 for _ in root.iter())
    print(f"  Загальна кількість елементів (включно з коренем): {count}")

if __name__ == "__main__":
    # Приклади запуску: python task4_processing.py ecb_rates.xml
    if len(sys.argv) < 2:
        print("Використання: python task4_processing.py <xmlfile>")
        sys.exit(1)
    xmlfile = sys.argv[1]
    if not os.path.exists(xmlfile):
        print("Файл не знайдено:", xmlfile)
        sys.exit(2)

    try:
        count_nodes(xmlfile)
        # Спробуємо визначити тип — якщо є 'Cube' з атрибутом time, вважатимемо ECB
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        if root.findall(".//Cube[@time]") or root.findall(".//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@time]"):
            parse_ecb_and_export_csv(xmlfile, csvfile="ecb_rates_export.csv")
            modify_and_write(xmlfile, outxml="ecb_rates_modified.xml")
        else:
            # Інший формат — спробуємо як RSS/ATOM
            rss_list_items(xmlfile, max_items=10)
            modify_and_write(xmlfile, outxml="feed_modified.xml")
    except Exception as e:
        print("Помилка при обробці:", e)