class Route:
    def __init__(self, start, finish, lengths):
        self.start = start
        self.finish = finish
        self.lengths = lengths

    def __str__(self):
        return f'\nНазва маршруту: {self.start}-{self.finish}({self.total_length()} км)\nКількість переходів: {self.num_transitions()}\nКількість привалів: {self.num_breaks()}'

    def total_length(self):
        return sum(self.lengths)

    def num_breaks(self):
        return len(self.lengths) - 1
    
    def num_transitions(self):
        return len(self.lengths)

    def longest_length(self):
        return max(self.lengths)

    def __lt__(self, other):
        return self.total_length() < other.total_length()

def max_breaks(routes):
    return max(routes, key=lambda route: route.num_breaks())

def max_transitions(routes):
    return max(routes, key=lambda route: route.num_transitions())

def longest_route(routes):
    return max(routes, key=lambda route: route.longest_length())

def routes_from_to(routes, point):
    return [route for route in routes if route.start == point or route.finish == point]    
