with open("data.txt", "w") as data:
    data.write("2\n5\n-3\n10\n4\n7\n-2\n6")

with open("data.txt", "r") as data:
    numbers = [int(line) for line in data.readlines()]
    average = sum(numbers) / len(numbers)

with open("result.txt", "w") as result:
    result.write(f"Arithmetic mean : {average}")