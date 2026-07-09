import re
import csv

def load_users():
    users = {
        'user1','password1',
        'user2', 'password2',
        # додайте більше користувачів тут
    }
    return users

def save_users(users):
    with open('users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Username", "Password"])
        for username, password in users.items():
            writer.writerow([username, password])

def check_password_strength(password):
    score = 0
    improvements = []
    
    if len(password) >= 8:
        score += 1
    else:
        improvements.append("Ваш пароль має бути не менше 8 символів.")
        
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        improvements.append("Ваш пароль повинен містити принаймні одну літеру у верхньому регістрі.")
        
    if re.search(r'[a-z]', password):
        score += 1
    else:
        improvements.append("Ваш пароль повинен містити принаймні одну літеру у нижньому регістрі.")
        
    if len(re.findall(r'\d', password)) >= 2:
        score += 1
    else:
        improvements.append("Ваш пароль повинен містити принаймні дві цифри.")
        
    if not re.search(r'[$%&@<>!]', password):
        score += 1
    else:
        improvements.append("Ваш пароль не повинен містити спеціальних символів ($, %, &, @, <, >, !).")
    
    return score, improvements

def delete_account(users):
    while True:
        username = input("Введіть ім'я користувача: ")
        if username not in users:
            print("Це ім'я користувача не зареєстровано. Будь ласка, спробуйте інше.")
            continue
        
        password = input("Введіть поточний пароль: ")
        if password != users[username]:
            print("Неправильний пароль. Будь ласка, спробуйте ще раз.")
            continue
        
        del users[username]
        print(f"Обліковий запис {username} успішно видалено.")
        
        break

def main():
    users = load_users()
    delete_account(users)
    save_users(users)

main()
