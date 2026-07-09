import string

def prepare_text(text):
    # Видаляємо пробіли, переводимо у верхній регістр, замінюємо J на I (для англійської)
    text = text.replace(" ", "").upper().replace("J", "I")
    # Для парності символів додаємо X, якщо довжина непарна
    if len(text) % 2 != 0:
        text += 'X'
    # Розбиваємо на біграми
    bigrams = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            bigrams.append(a + 'X')
            i += 1
        else:
            bigrams.append(a + b)
            i += 2
    return bigrams

def generate_matrix(key):
    alphabet = string.ascii_uppercase.replace('J', '') # Playfair ігнорує J
    matrix = []
    used = set()
    key = key.upper().replace("J", "I")
    for c in key:
        if c in alphabet and c not in used:
            matrix.append(c)
            used.add(c)
    for c in alphabet:
        if c not in used:
            matrix.append(c)
            used.add(c)
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def playfair_encrypt(bigrams, matrix):
    result = ""
    for bigram in bigrams:
        a, b = bigram[0], bigram[1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            # Один рядок, беремо праворуч
            result += matrix[row_a][(col_a+1)%5] + matrix[row_b][(col_b+1)%5]
        elif col_a == col_b:
            # Один стовпчик, беремо нижче
            result += matrix[(row_a+1)%5][col_a] + matrix[(row_b+1)%5][col_b]
        else:
            # Прямокутник
            result += matrix[row_a][col_b] + matrix[row_b][col_a]
    return result

def playfair_decrypt(bigrams, matrix):
    result = ""
    for bigram in bigrams:
        a, b = bigram[0], bigram[1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            result += matrix[row_a][(col_a-1)%5] + matrix[row_b][(col_b-1)%5]
        elif col_a == col_b:
            result += matrix[(row_a-1)%5][col_a] + matrix[(row_b-1)%5][col_b]
        else:
            result += matrix[row_a][col_b] + matrix[row_b][col_a]
    return result

def main():
    mode = input("Оберіть режим (e - шифрувати, d - розшифрувати): ").strip()
    key = input("Введіть ключове слово: ").strip()
    if mode == 'e':
        input_file = input("Введіть назву вхідного файлу: ").strip()
        output_file = input("Введіть назву вихідного файлу: ").strip()
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        bigrams = prepare_text(text)
        matrix = generate_matrix(key)
        encrypted = playfair_encrypt(bigrams, matrix)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        print("Зашифрований текст записано у:", output_file)
    elif mode == 'd':
        input_file = input("Введіть назву файлу із зашифрованим текстом: ").strip()
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted = f.read()
        bigrams = prepare_text(encrypted)
        matrix = generate_matrix(key)
        decrypted = playfair_decrypt(bigrams, matrix)
        print("Розшифрований текст:\n", decrypted)
    else:
        print("Невірний режим!")

if __name__ == "__main__":
    main()