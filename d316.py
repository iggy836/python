def find_min_temperature():
    temperatures = []
    for _ in range(4):
        temp = int(input().strip())
        temperatures.append(temp)
    print(min(temperatures))

find_min_temperature()
