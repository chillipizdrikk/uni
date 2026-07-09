from functions import Route, max_breaks, max_transitions, longest_route, routes_from_to

routes = ['Kvasy,Dzembronya,8,8,12,18,12\n',
          'Dzembronya,PipIvan,5,7,12,18\n',
          'VusokuyKamin,Pikuy,10,8,9,10,8,10\n',
          'Pikuy,Parashka,10,7,8,11\n',
          'Gemba,Kvasy,5,7,12,16,20\n']

with open('routes.txt', 'w') as file:
    file.writelines(routes)
    
routes = []
with open('routes.txt', 'r') as file:
    for line in file:
        data = line.strip().split(',')
        start = data[0]
        finish = data[1]
        lengths = list(map(int, data[2:]))
        routes.append(Route(start, finish, lengths))

routes.sort()

print('\n-----Всі маршрути-----')
for route in routes:
    print(route)
print('------------------------')

print(f'Маршрут з максимальною кількістю привалів: {max_breaks(routes)}\n')
print(f'Маршрут з максимальною кількість переходів: {max_transitions(routes)}\n')
print(f'Маршрут з найдовшим переходом: {longest_route(routes)}\n')

point = input('Будь ласка, введіть точку, в якій починається або закінчується маршрут: ')
routes_point = routes_from_to(routes, point)
if routes_point:
    print(f'Ось можливі маршрути, що починаються або закінчуються в {point}:')
    for route in routes_point:
        print(route)
else:
    print(f'Немає маршрутів, що починаються або закінчуються в {point}')