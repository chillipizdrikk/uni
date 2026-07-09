import numpy as np

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_LEN = len(ALPHABET) 

def preprocess_text(text):
        text = text.upper()
        return "".join([char for char in text if char in ALPHABET])

def text_to_numbers(text):
        return [ALPHABET.find(char) for char in text]

def numbers_to_text(numbers):
        return "".join([ALPHABET[num] for num in numbers])

def generate_key_matrix(key_word, n=3):
        key_numbers = text_to_numbers(key_word[:n*n])
        if len(key_numbers) < n*n:
                raise ValueError(f"Ключове слово має містити щонайменше {n*n} літер.")

        key_matrix = np.array(key_numbers).reshape(n, n)
        det = int(round(np.linalg.det(key_matrix))) % ALPHABET_LEN

        import math
        if math.gcd(det, ALPHABET_LEN) != 1:
                raise ValueError("Визначник матриці не взаємно простий з довжиною алфавіту. Спробуйте інше ключове слово.")
        
        print("\nЗгенерована ключ-матриця:")
        print(key_matrix)
        return key_matrix

def mod_inverse(a, m):
        for x in range(1, m):
                if (a * x) % m == 1:
                        return x
        return None

def find_inverse_matrix(matrix):
        det = int(round(np.linalg.det(matrix)))
        det_inv = mod_inverse(det, ALPHABET_LEN)
        if det_inv is None:
                raise ValueError("Не вдалося знайти обернене значення визначника.")
        
        adjugate = np.round(det * np.linalg.inv(matrix)).astype(int)
        inverse_matrix = (adjugate * det_inv) % ALPHABET_LEN
        return inverse_matrix

def hill_encrypt(plaintext, key_matrix):
        n = key_matrix.shape[0]
        plain_numbers = text_to_numbers(plaintext)
        if len(plain_numbers) % n != 0:
                plain_numbers += [0] * (n - (len(plain_numbers) % n))
        
        ciphertext_numbers = []
        for i in range(0, len(plain_numbers), n):
                block = np.array(plain_numbers[i:i+n])
                encrypted_block = np.dot(key_matrix, block) % ALPHABET_LEN
                ciphertext_numbers.extend(encrypted_block)
        
        return numbers_to_text(ciphertext_numbers)

def hill_decrypt(ciphertext, key_matrix):
        n = key_matrix.shape[0]
        try:
                inverse_key_matrix = find_inverse_matrix(key_matrix)
                print("\nЗгенерована обернена ключ-матриця:")
                print(inverse_key_matrix)
        except ValueError as e:
                print(e)
                return "Не вдалося розшифрувати."

        cipher_numbers = text_to_numbers(ciphertext)
        
        decrypted_numbers = []
        for i in range(0, len(cipher_numbers), n):
                block = np.array(cipher_numbers[i:i+n])
                decrypted_block = np.dot(inverse_key_matrix, block) % ALPHABET_LEN
                decrypted_numbers.extend(decrypted_block)
        
        return numbers_to_text(decrypted_numbers)

if __name__ == "__main__":
        file_path_plaintext = "plaintext.txt"
        file_path_ciphertext = "ciphertext.txt"
        print("1. Шифрування повідомлення:")
        try:
                with open(file_path_plaintext, "r", encoding="utf-8") as file:
                        plaintext_raw = file.read()
                
                plaintext = preprocess_text(plaintext_raw)
                key_word = input("Введіть ключове слово (9 або більше літер): ")
                key_matrix = generate_key_matrix(key_word, n=3)
                ciphertext = hill_encrypt(plaintext, key_matrix)
                with open(file_path_ciphertext, "w", encoding="utf-8") as file:
                        file.write(ciphertext)

                print(f"\nШифрування успішно завершено. Шифрограму збережено у файл '{file_path_ciphertext}'.")
        
        except FileNotFoundError:
                print(f"Помилка: Файл '{file_path_plaintext}' не знайдено.")
        except ValueError as e:
                print(f"Помилка: {e}")
        
        print("\n" + "="*50 + "\n")
        
        print("2. Розшифрування повідомлення:")
        try:
                with open(file_path_ciphertext, "r", encoding="utf-8") as file:
                        ciphertext_read = file.read()
                key_word_decrypt = input("Введіть ключове слово для розшифрування: ")
                key_matrix_decrypt = generate_key_matrix(key_word_decrypt, n=3)
                decrypted_text = hill_decrypt(ciphertext_read, key_matrix_decrypt)
                print("\nРозшифрований текст:")
                print(decrypted_text)
                with open("decrypted.txt", "w", encoding="utf-8") as file:
                        file.write(decrypted_text)
                print("\nРозшифрований текст збережено у файл 'decrypted.txt'.")
                
        except FileNotFoundError:
                print(f"Помилка: Файл '{file_path_ciphertext}' не знайдено. Спочатку виконайте шифрування.")
        except ValueError as e:
                print(f"Помилка: {e}")
