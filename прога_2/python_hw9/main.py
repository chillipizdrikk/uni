import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('anime.csv')

df.columns = ['Аніме', 'Дата випуску', 'Тривалість', 'Жанр', 'Рейтинг']
print(df.head(10)) 

#Первинний статистичний аналіз
description = df.describe()
print("\nПервинний статистичний аналіз:")
print(f"Кількість ненульових спостережень: {description['Рейтинг']['count']}")
print(f"Середнє значення: {description['Рейтинг']['mean']}")
print(f"Стандартне відхилення: {description['Рейтинг']['std']}")
print(f"Мінімальне значення: {description['Рейтинг']['min']}")
print(f"Перший квартиль (25% спостережень менше за це значення): {description['Рейтинг']['25%']}")
print(f"Медіана (середнє значення): {description['Рейтинг']['50%']}")
print(f"Третій квартиль (75% спостережень менше за це значення): {description['Рейтинг']['75%']}")
print(f"Максимальне значення: {description['Рейтинг']['max']}\n")

#Групування
grouped = df.groupby('Жанр')['Рейтинг'].mean().reset_index()
grouped.columns = ['Жанр', 'Середній рейтинг']
print(grouped)

#Візуалізація 
plt.figure(figsize=(10,5))
plt.hist(df['Рейтинг'], bins=20, color='skyblue', edgecolor='black')
plt.title('Гістограма рейтингів')
plt.xlabel('Рейтинг')
plt.ylabel('Кількість')
plt.show()

genres = df['Жанр'].unique()
for genre in genres:
    df_genre = df[df['Жанр'] == genre]
    plt.figure(figsize=(10,10))
    df_genre['Рейтинг'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title(f'Кругова діаграма рейтингів для жанру {genre}')
    plt.ylabel('')
    plt.show()
