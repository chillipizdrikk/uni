import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 32

# Зовнішній багатокутник (зіркоподібна фігура)
outer_polygon = [
    (16, 30), (12, 25), (6, 26), (10, 20), (4, 14), (12, 15),
    (16, 8), (20, 15), (28, 14), (22, 20), (26, 26), (20, 25), (16, 30)
]

# Внутрішній багатокутник (ромб)
inner_polygon = [
    (16, 22), (14, 18), (16, 14), (18, 18), (16, 22)
]

# Затравочний піксель
seed_pixel = (14, 20)


def point_in_polygon(x: int, y: int, polygon: list[tuple[int, int]]) -> bool:
    """Перевіряє, чи точка (x, y) знаходиться всередині багатокутника, заданого списком координат polygon."""
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def on_edge(x: int, y: int, polygon: list[tuple[int, int]]) -> bool:
    """Перевіряє, чи точка (x, y) знаходиться на одному з ребер багатокутника polygon."""
    n = len(polygon)
    for i in range(n - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        if (min(x1, x2) <= x <= max(x1, x2)) and (min(y1, y2) <= y <= max(y1, y2)):
            if (x2 - x1) * (y - y1) == (y2 - y1) * (x - x1):  # Перевірка на колінеарність точки та ребра
                return True
    return False

def is_inside(x: int, y: int) -> bool:
    """Перевіряє, чи точка (x, y) знаходиться всередині зовнішнього полігону та поза внутрішнім полігоном."""
    return (
        point_in_polygon(x + 0.5, y + 0.5, outer_polygon) and 
        not point_in_polygon(x + 0.5, y + 0.5, inner_polygon) 
    )

def seed_fill(seed_pixel: tuple[int, int]) -> set[tuple[int, int]]:
    """Алгоритм заливки, який заповнює всі пікселі в межах зовнішнього полігону, що не знаходяться всередині внутрішнього полігону."""
    x, y = seed_pixel
    filled_pixels = set()
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        if (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) and ((x, y) not in filled_pixels) and is_inside(x, y):
            filled_pixels.add((x, y))
            stack.extend([(x, y+1), (x, y-1), (x+1, y), (x-1, y)])

    return filled_pixels

filled_pixels = seed_fill(seed_pixel)

grid = np.zeros((GRID_SIZE, GRID_SIZE))

for x, y in filled_pixels:
    grid[y, x] = 1

fig, ax = plt.subplots(figsize=(8, 8))

ax.imshow(grid, cmap='Wistia', origin='lower', extent=[0, GRID_SIZE, 0, GRID_SIZE], interpolation='none')

outer_x, outer_y = zip(*outer_polygon + [outer_polygon[0]])
ax.plot(outer_x, outer_y, color="black", linewidth=2, label="Outer Polygon")

inner_x, inner_y = zip(*inner_polygon + [inner_polygon[0]])
ax.plot(inner_x, inner_y, color="green", linewidth=2, label="Inner Polygon")

ax.plot(seed_pixel[0], seed_pixel[1], marker="o", color="red", markersize=8, label="Seed Pixel")

ax.set_xticks(np.arange(0, GRID_SIZE, 1))
ax.set_yticks(np.arange(0, GRID_SIZE, 1))

ax.set_xticklabels([str(i) for i in range(GRID_SIZE)])
ax.set_yticklabels([str(i) for i in range(GRID_SIZE)])

ax.grid(color='gray', linestyle='--', linewidth=0.5)
ax.legend()

plt.show()