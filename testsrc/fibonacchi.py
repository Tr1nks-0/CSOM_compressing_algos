def fibonacchi(n1=0, n2=1):
    while True:
        yield n1
        n1, n2 = n2, n1 + n2


if __name__ == '__main__':
    f = fibonacchi(1, 2)
    data = bytearray()
    for number in range(256):
        for index in range(number):
            data.append(number)
    with open('C:/W/controlsSystemOptimisationMethods/resources/in_fib', 'wb') as file:
        file.write(data)
