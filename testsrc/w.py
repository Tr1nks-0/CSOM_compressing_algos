def walk(i):
    if isinstance(i, list):
        print('nest')
        for ii in i:
            for iii in walk(ii):
                yield iii
    else:
        yield i
        # return i


if __name__ == '__main__':
    arr = [1, 2, [3, 4, 5], 6, [7, 8]]
    for n in walk(arr):
        print(n)
