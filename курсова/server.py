# #server
# from socket import *
# import threading

# address = 'localhost'
# port = 8086
# ip_end = (address, port)

# listener = socket(AF_INET, SOCK_STREAM)
# listener.bind(ip_end)
# listener.listen(5)
# print("Очікування...")

# def hadler(client):
#     result=0
#     for i in range(3):
#         data =client.recv(1024)
#         number = int(data.decode())
#         result += number
#     message = str(result).encode()
#     client.send(message)
#     print("Результат відправлено")
#     client.close()

# def threader():
#     while True:
#         s, ip_addr = listener.accept()
#         print(f"З'єднано з {ip_addr}")
#         threading.Thread(target=hadler, args=(s,)).start()

# threader()

from socket import *
import threading

address = 'localhost'
port = 8086
ip_end = (address, port)

listener = socket(AF_INET, SOCK_STREAM)
listener.bind(ip_end)
listener.listen(5)
print("Сервер працює, очікування клієнтів...")

def handle_client(client, ip_addr):
    """Обробка окремого клієнта."""
    print(f"З'єднано з {ip_addr}\nВведіть повідомлення:")

    def receive_messages():
        while True:
            try:
                data = client.recv(1024).decode()
                if not data:
                    break
                print(f"Клієнт: {data}")
            except:
                print(f"З'єднання з {ip_addr} розірвано")
                break

    # Запуск потоку для отримання повідомлень від клієнта
    threading.Thread(target=receive_messages, daemon=True).start()

    try:
        while True:
            message = input()  # Введення повідомлення сервером
            if message.lower() == 'exit':
                print("Завершення з'єднання з клієнтом...")
                break
            client.send(message.encode())  # Відправка повідомлення клієнту
    finally:
        client.close()
        print(f"З'єднання з {ip_addr} закрите")

def threader():
    """Прослуховування нових клієнтів."""
    while True:
        client, ip_addr = listener.accept()
        threading.Thread(target=handle_client, args=(client, ip_addr)).start()

try:
    threader()
except KeyboardInterrupt:
    print("\nСервер зупинено вручну")
finally:
    listener.close()
    print("Сервер вимкнено")
