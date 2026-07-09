import matplotlib.pyplot as plt
import numpy as np

def find_intersection(func1, func2, x_range):
    for x in x_range:
        if np.isclose(func1(x), func2(x), atol=1e-2):
            return (x, func1(x))
    return None

def main():
    x = np.linspace(-15, 15, 200)
    y1 = (11 - x) / 2
    y2 = 6 - x
    y3 = x - 2
    y4 = (2 * x + 4) / 4
    
    plt.plot(x, y1, label='x1+2x2<=11')
    plt.plot(x, y2, label='x1+x2<=6')
    plt.plot(x, y3, label='x1-x2<=2')
    plt.plot(x, y4, label='-2x1+4x2>=4')

    plt.xlim(-2, 10)
    plt.ylim(-3, 7)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend(loc='upper right')

    plt.xticks(np.arange(-2, 11, 1))
    plt.yticks(np.arange(-3, 8, 1))
    plt.grid(which='both')

    plt.axhline(y=0, color='black', linewidth=1.5)
    plt.axvline(x=0, color='black', linewidth=1.5)

    # Знайти точки перетину
    intersections = [
        find_intersection(lambda x: (11 - x) / 2, lambda x: 6 - x, np.linspace(-15, 15, 200)),
        find_intersection(lambda x: (11 - x) / 2, lambda x: x - 2, np.linspace(-15, 15, 200)),
        find_intersection(lambda x: (11 - x) / 2, lambda x: (2 * x + 4) / 4, np.linspace(-15, 15, 200)),
        find_intersection(lambda x: 6 - x, lambda x: x - 2, np.linspace(-15, 15, 200)),
        find_intersection(lambda x: 6 - x, lambda x: (2 * x + 4) / 4, np.linspace(-15, 15, 200)),
        find_intersection(lambda x: x - 2, lambda x: (2 * x + 4) / 4, np.linspace(-15, 15, 200)),
    ]

    # Додати точки перетину на графік
    for point in intersections:
        if point:
            plt.plot(point[0], point[1], 'ro')

    plt.show()

if __name__ == '__main__':
    main()
