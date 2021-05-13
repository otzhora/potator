def some_func1(a):
    s = 0
    for x in a:
        s += x
    return s


if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5]
    print(some_func1(lst))
