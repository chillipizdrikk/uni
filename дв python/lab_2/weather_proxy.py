import collections
import statistics

def parse_weather_file(filename):
    """
    Зчитує дані з текстового файлу та створює словник, що містить усі показники погоди.
    Формат файлу: місто, дата, час, температура, тиск, напрямок вітру (через табуляцію).
    """
    weather_dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) != 6:
                continue
            city, date, time, temp, pressure, wind = fields
            try:
                temp = int(temp)
                pressure = int(pressure)
            except ValueError:
                continue
            # Структура: weather_dict[city][date][time] = { 'temp': ..., 'pressure': ..., 'wind': ... }
            weather_dict[city][date][time] = {'temp': temp, 'pressure': pressure, 'wind': wind}
    return weather_dict

def show_city_weather(weather_dict, city, date=None):
    """
    Відображає всі погодні показники для заданого міста.
    """
    result = []
    if city not in weather_dict:
        return f"Дані для міста {city} не знайдено."
    dates = [date] if date else weather_dict[city].keys()
    for d in dates:
        for t, vals in weather_dict[city][d].items():
            result.append(f"{city}, {d}, {t}: Темп={vals['temp']}°C, Тиск={vals['pressure']} мм, Вітер={vals['wind']}")
    return '\n'.join(result) if result else f"Дані для {city} на {date} не знайдено."

def get_city_with_extreme_temp(weather_dict, highest=True):
    """
    Знаходить місто з найвищою/найнижчою температурою серед усіх записів.
    """
    extreme = None
    city_name = None
    for city in weather_dict:
        for date in weather_dict[city]:
            for time, vals in weather_dict[city][date].items():
                temp = vals['temp']
                if extreme is None or (highest and temp > extreme) or (not highest and temp < extreme):
                    extreme = temp
                    city_name = city
    return f"{'Найвища' if highest else 'Найнижча'} температура: {extreme}°C у місті {city_name}"

def temp_dynamics_in_city(weather_dict, city, date):
    """
    Динаміка зміни температури по годинах для міста і дати.
    """
    if city not in weather_dict or date not in weather_dict[city]:
        return f"Дані для {city} на {date} не знайдено."
    times = sorted(weather_dict[city][date].keys())
    temps = [weather_dict[city][date][t]['temp'] for t in times]
    result = [f"{t}: {temp}°C" for t, temp in zip(times, temps)]
    return f"Динаміка температури в {city} {date}:\n" + "\n".join(result)

def prevailing_wind_direction(weather_dict, cities=None):
    """
    Визначає переважаючий напрямок вітру серед обраних міст (або всіх).
    """
    winds = []
    target_cities = cities if cities else weather_dict.keys()
    for city in target_cities:
        for date in weather_dict[city]:
            for time in weather_dict[city][date]:
                winds.append(weather_dict[city][date][time]['wind'])
    if not winds:
        return "Немає даних про напрямок вітру."
    most_common = collections.Counter(winds).most_common(1)[0]
    return f"Переважаючий напрямок вітру: {most_common[0]} ({most_common[1]} випадків)"

def cities_below_temp(weather_dict, t):
    """
    Повертає список міст, де температура нижча за t в будь-який момент часу.
    """
    result = set()
    for city in weather_dict:
        for date in weather_dict[city]:
            for time, vals in weather_dict[city][date].items():
                if vals['temp'] < t:
                    result.add(city)
                    break
    return f"Міста з температурою нижче {t}°C: {', '.join(result)}" if result else "Немає таких міст."

def write_results_to_file(results, filename):
    """
    Записує результати аналізу в текстовий файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(results)

# Приклад самостійного тестування та виконання задач
if __name__ == "__main__":
    # Завантаження даних
    weather = parse_weather_file("weather_data.txt")

    # 1. Відобразити дані для міста
    print(show_city_weather(weather, "Одеса"))

    # 2. Найвища температура
    print(get_city_with_extreme_temp(weather, highest=True))

    # 3. Динаміка температури у Львові
    print(temp_dynamics_in_city(weather, "Дніпро", "2025-09-28"))

    # 4. Переважаючий вітер
    print(prevailing_wind_direction(weather))

    # 5. Міста з похолоданням (t < 13)
    print(cities_below_temp(weather, 13))

    # 6. Запис результатів у файл
    res = "\n".join([
        show_city_weather(weather, "Одеса"),
        get_city_with_extreme_temp(weather, highest=True),
        temp_dynamics_in_city(weather, "Дніпро", "2025-09-28"),
        prevailing_wind_direction(weather),
        cities_below_temp(weather, 13)
    ])
    write_results_to_file(res, "weather_results.txt")