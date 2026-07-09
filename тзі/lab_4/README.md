```markdown
# Варіант 2 — Ель-Гамаль + RSA підпис (Python)

Цей набір скриптів реалізує:
- Асиметричну криптосистему Ель-Гамаля (генерація ключів, шифрування, розшифрування).
- Цифровий підпис на основі RSA (генерація ключів, підписування, перевірка).

Реалізація чисто на Python без зовнішніх залежностей. Генерація простих чисел використовує тест Миллера—Рабіна.

Файли:
- elgamal_rsa.py — головний скрипт (CLI).
- message.txt — приклад відкритого повідомлення.

Приклади використання (у терміналі):

1) Генерація ключів Ель-Гамаля:
   python elgamal_rsa.py elgamal-gen-keys --out-prefix elgamal --p-bits 2048

   Це збереже:
   - elgamal_pub.json  (p, g, h)
   - elgamal_priv.json (a)

2) Шифрування повідомлення (читає message.txt -> записує ciphertext_elgamal.json):
   python3 elgamal_rsa.py elgamal-encrypt --pub elgamal_pub.json --in message.txt --out ciphertext_elgamal.json

3) Генерація RSA ключів для підпису:
   python3 elgamal_rsa.py rsa-gen-keys --out-prefix rsa --p-bits 1024 --q-bits 1024

   Це збереже:
   - rsa_pub.json  (n, e)
   - rsa_priv.json (d)

4) Підписування файлу:
   python3 elgamal_rsa.py rsa-sign --priv rsa_priv.json --in message.txt --out signature.json

   signature.json містить підпис та RSA public (n, e).

5) Перевірка підпису та розшифрування:
   python3 elgamal_rsa.py verify --ciphertext ciphertext_elgamal.json --elgamal-priv elgamal_priv.json --signature signature.json

   Команда:
   - розшифрує повідомлення за допомогою ElGamal (приватного a),
   - обчислить хеш повідомлення,
   - перевірить RSA-підпис (за n,e зі signature.json),
   - виведе висновок про істинність підпису і збережене розшифроване повідомлення (виводиться в stdout).

Формати файлів:
- JSON з великими числами зберігаються як рядки (decimal).
- ciphertext_elgamal.json:
  {
    "p": "...",
    "g": "...",
    "h": "...",
    "ciphertext": [
      ["c1_1", "c2_1"],
      ["c1_2", "c2_2"],
      ...
    ]
  }
- signature.json:
  {
    "n": "...",
    "e": "...",
    "signature": "..."
  }

Примітки:
- Для шифрування повідомлення розбивається на блоки, розмір блоку визначається з p (щоб int(block) < p).
- Генерація великих простих може зайняти час (особливо для 2048-bit p). Можна зменшити розмір біт за допомогою параметрів.
```