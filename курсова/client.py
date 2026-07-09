# #client
# from socket import *

# address = 'localhost'
# port = 8086
# ip_end = (address, port)

# s = socket(AF_INET, SOCK_STREAM)
# s.connect(ip_end)
# print("З'єднання встановлено")

# print("Введіть три числа:")
# for i in range(3):
#     number = int(input(f"n_{i+1} = "))
#     message = str(number).encode() 
#     s.send(message)
#     print(f"Число {i+1} відправлене")
# print("Усі числа відправлені\n")

# data = s.recv(1024)
# result = data.decode()
# print(f"Обчислена віддалено сума дорівнює {result}")
# s.close()


from socket import *
import threading

address = 'localhost'
port = 8086
ip_end = (address, port)

s = socket(AF_INET, SOCK_STREAM)
s.connect(ip_end)
print("З'єднання встановлено\nВведіть повідомлення:")

#функція для отримання повідомлень від сервера
def receive_messages():
    while True:
        try:
            response = s.recv(1024).decode()
            if not response:
                break
            print(f"Сервер: {response}")
        except:
            print("З'єднання з сервером розірвано")
            break

#запуск потоку для отримання повідомлень
threading.Thread(target=receive_messages, daemon=True).start()

try:
    while True:
        message = input()  
        if message.lower() == 'exit':
            print("Завершення з'єднання...")
            break
        s.send(message.encode())  #надсилання повідомлення серверу
finally:
    s.close()
    print("З'єднання закрите")
