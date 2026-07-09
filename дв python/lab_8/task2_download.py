"""
Сценарій веб-клієнта — задача 2
- Завантажує вказану веб-сторінку або файл за URL.
- Робить трасування (print), обробку помилок і просту логіку повторних спроб.
- Зберігає файл у поточну директорію з іменем, виведеним з URL або заголовка.
"""

import requests
import time
import os
import sys
from urllib.parse import urlparse, unquote
import mimetypes

def filename_from_url(url, resp):
    # Спроба отримати ім'я з Content-Disposition
    cd = resp.headers.get('content-disposition')
    if cd:
        import re
        m = re.search(r'filename=["\']?([^"\';]+)', cd)
        if m:
            return m.group(1)
    # Інакше — остання частина шляху
    path = urlparse(url).path
    name = os.path.basename(path) or "downloaded"
    name = unquote(name)
    # Додати розширення залежно від content-type
    ctype = resp.headers.get('content-type','')
    ext = ''
    if '.' not in name:
        ext = mimetypes.guess_extension(ctype.split(';')[0].strip() or '')
        if ext:
            name += ext
    return name

def download(url, max_retries=3, delay=10, timeout=15):
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Спроба {attempt} завантажити: {url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; example-script/1.0; +https://example.local/)"
            }
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            print(f"  HTTP {resp.status_code}  Content-Type: {resp.headers.get('content-type')}")
            resp.raise_for_status()
            name = filename_from_url(url, resp)
            fname = os.path.abspath(name)
            with open(fname, "wb") as f:
                f.write(resp.content)
            print(f"  Успішно збережено в: {fname}  (байт: {len(resp.content)})")
            return fname
        except requests.exceptions.RequestException as e:
            print(f"  Помилка: {e}")
            if attempt < max_retries:
                print(f"  Чекаю {delay} секунд перед повтором...")
                time.sleep(delay)
            else:
                print("  Досягнуто максимум спроб. Завершую.")
                raise
    raise RuntimeError("Невдалося завантажити файл")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = input("Введіть повний URL (наприклад https://www.python.org/): ").strip()
    try:
        saved = download(url)
        print("Відкрийте збережений файл будь-яким браузером або редактором.")
    except Exception as e:
        print("Сценарій завершився з помилкою:", e)
