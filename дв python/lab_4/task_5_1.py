from protected_stack import ProtectedStack

def move_between_rods(rods, from_idx, to_idx, moves):
    from_rod = rods[from_idx]
    to_rod = rods[to_idx]
    if from_rod.is_empty(): 
        disk = to_rod.pop()
        from_rod.push(disk)
        moves.append((to_idx, from_idx, disk))
    elif to_rod.is_empty():
        disk = from_rod.pop()
        to_rod.push(disk)
        moves.append((from_idx, to_idx, disk))
    else:
        top_from = from_rod.peek()
        top_to = to_rod.peek()
        if top_from < top_to:
            disk = from_rod.pop()
            to_rod.push(disk)
            moves.append((from_idx, to_idx, disk))
        else:
            disk = to_rod.pop()
            from_rod.push(disk)
            moves.append((to_idx, from_idx, disk))

def hanoi_iterative(n):
    rods = [ProtectedStack() for _ in range(3)]
    for disk in range(n, 0, -1):
        rods[0].push(disk)
    moves = []
    total_ops = 0
    if n % 2 == 0:
        order = [(0,1),(0,2),(1,2)]
    else:
        order = [(0,2),(0,1),(1,2)]
    num_moves = 2**n - 1
    for i in range(1, num_moves+1):
        from_idx, to_idx = order[(i-1)%3]
        move_between_rods(rods, from_idx, to_idx, moves)
        total_ops += 1
    return moves, total_ops

def run_tests():
    for n in [1,2,3,4]:
        moves, ops = hanoi_iterative(n)
        print(f"{n} дисків: операцій {ops}, перших кроків: {moves[:min(len(moves),8)]}")

if __name__ == "__main__":
    run_tests()