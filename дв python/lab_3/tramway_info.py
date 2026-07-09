"""
Інформаційно-довідкова система про трамваї Львова з меню вибору типу запиту.
"""
tramway = {
    1: [
        [
            "Залізничний вокзал",
            "Приміський вокзал",
            "Кропивницького",
            "Старосольських",
            "Львівська політехніка",
            "Головна пошта",
            "Дорошенка",
            "Площа Ринок",
            "Руська",
            "Площа Митна",
            "Військовий госпіталь",
            "Медичний університет",
            "Мечникова",
            "Меморіал",
            "Личаківський цвинтар",
            "Інфекційна лікарня",
            "Левицького",
            "Погулянка"
        ],
        [],
        set(),
    ],
    8: [
        [
            "Вернадського",
            "Санта Барбара",
            "Коломийська",
            "Четверта поліклініка",
            "Довженка",
            "Дитяча поліклініка",
            "Шувар",
            "Угорська",
            "Стадіон Україна",
            "Академія Мистецтв",
            "Стрийський парк",
            "Площа Франка",
            "Саксаганського",
            "Шухевича",
            "Площа Соборна"
        ],
        [],
        set(),
    ]
}

for route, value in tramway.items():
    value[1] = value[0][::-1]
    value[2] = set(value[0])

def find_routes_through_stop(stop_name):
    res = []
    for route, val in tramway.items():
        if stop_name in val[2]:
            res.append(route)
    return res

def stops_on_route(route, from_stop, to_stop):
    stops = tramway[route][0]
    if from_stop in stops and to_stop in stops:
        i, j = stops.index(from_stop), stops.index(to_stop)
        if i < j:
            return stops[i:j+1]
        else:
            stops_rev = tramway[route][1]
            i, j = stops_rev.index(from_stop), stops_rev.index(to_stop)
            return stops_rev[i:j+1]
    return []

def show_route_from_to(from_stop, to_stop):
    possible = []
    for route, val in tramway.items():
        if from_stop in val[2] and to_stop in val[2]:
            stops = stops_on_route(route, from_stop, to_stop)
            if stops:
                possible.append((route, stops))
    if possible:
        route, stops = min(possible, key=lambda x: len(x[1]))
        return f'Сідайте на трамвай {route} на зупинці "{from_stop}" і їдьте до "{to_stop}". Кількість зупинок: {len(stops)-1}.'
    for r1, v1 in tramway.items():
        if from_stop not in v1[2]:
            continue
        for r2, v2 in tramway.items():
            if r1 == r2 or to_stop not in v2[2]:
                continue
            common = v1[2] & v2[2]
            for transfer in common:
                if transfer != from_stop and transfer != to_stop:
                    stops1 = stops_on_route(r1, from_stop, transfer)
                    stops2 = stops_on_route(r2, transfer, to_stop)
                    if stops1 and stops2:
                        return (
                            f'Сідайте на трамвай {r1} на зупинці "{from_stop}" до "{transfer}" ({len(stops1)-1} зупинок), '
                            f'пересідайте на трамвай {r2} до "{to_stop}" ({len(stops2)-1} зупинок).'
                        )
    return "Прямого маршруту немає. Потрібна пересадка, або маршрут не знайдено."

def can_reach(from_stop, to_stop):
    for route, val in tramway.items():
        if from_stop in val[2] and to_stop in val[2]:
            return True, []
    for r1, v1 in tramway.items():
        if from_stop not in v1[2]:
            continue
        for r2, v2 in tramway.items():
            if r1 == r2 or to_stop not in v2[2]:
                continue
            if v1[2] & v2[2]:
                return True, [r1, r2]
    return False, []

def stops_count(from_stop, to_stop):
    for route, val in tramway.items():
        if from_stop in val[2] and to_stop in val[2]:
            stops = stops_on_route(route, from_stop, to_stop)
            if stops:
                return len(stops)-1, route
    return None, None

def tram_through_stops(*stops):
    res = []
    for route, val in tramway.items():
        if all(stop in val[2] for stop in stops):
            res.append(route)
    return res

def validate_stop(stop):
    for val in tramway.values():
        if stop in val[2]:
            return True
    return False

def print_stops():
    all_stops = set()
    for v in tramway.values():
        all_stops |= v[2]
    print("Список всіх зупинок:")
    for s in sorted(all_stops):
        print(" -", s)

def main():
    while True:
        print("\nОберіть тип запиту:")
        print("1. Як переїхати від зупинки до зупинки?")
        print("2. Чи можна потрапити від зупинки до зупинки?")
        print("3. Скільки зупинок між двома зупинками?")
        print("4. Якими трамваями можна доїхати на зупинку?")
        print("5. Який трамвай має маршрут через перелік зупинок?")
        print("6. Показати список усіх зупинок")
        print("0. Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == "0":
            print("Дякуємо за користування системою!")
            break
        elif choice == "1":
            from_stop = input('Введіть назву зупинки відправлення: ').strip()
            to_stop = input('Введіть назву зупинки призначення: ').strip()
            if not (validate_stop(from_stop) and validate_stop(to_stop)):
                print("Одну з обраних зупинок не знайдено.")
                continue
            print(show_route_from_to(from_stop, to_stop))
        elif choice == "2":
            from_stop = input('Введіть назву зупинки відправлення: ').strip()
            to_stop = input('Введіть назву зупинки призначення: ').strip()
            if not (validate_stop(from_stop) and validate_stop(to_stop)):
                print("Одну з обраних зупинок не знайдено.")
                continue
            ok, routes = can_reach(from_stop, to_stop)
            if ok and not routes:
                print("Можна без пересадки.")
            elif ok and routes:
                print(f"Можна, з пересадкою з трамваю {routes[0]} на трамвай {routes[1]}.")
            else:
                print("Не можна.")
        elif choice == "3":
            from_stop = input('Введіть назву зупинки відправлення: ').strip()
            to_stop = input('Введіть назву зупинки призначення: ').strip()
            num, route = stops_count(from_stop, to_stop)
            if num is not None:
                print(f"{num} зупинок без пересадки трамваєм {route}.")
            else:
                print("Потрібна пересадка або маршрут неможливий.")
        elif choice == "4":
            stop = input('Введіть назву зупинки: ').strip()
            if not validate_stop(stop):
                print("Зупинку не знайдено в переліку трамвайних маршрутів.")
                continue
            trams = find_routes_through_stop(stop)
            if trams:
                print("Трамваї:", ", ".join(map(str, trams)))
            else:
                print("Жоден трамвай не зупиняється на цій зупинці.")
        elif choice == "5":
            stops = input('Введіть перелік зупинок через кому: ').split(",")
            stops = [s.strip() for s in stops if s.strip()]
            if not all(validate_stop(stop) for stop in stops):
                print("Одна з вказаних зупинок не існує.")
                continue
            trams = tram_through_stops(*stops)
            if trams:
                print(f"Трамвай(ї): {', '.join(map(str, trams))}")
            else:
                print("Жоден трамвай не проходить через усі ці зупинки.")
        elif choice == "6":
            print_stops()
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()