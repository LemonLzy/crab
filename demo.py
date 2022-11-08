def random_no1():
    head = "22118800"
    result = []
    first = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    second = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    last = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in first:
        for j in second:
            for m in last:
                res = head + str(i) + "0" + str(j) + str(m)
                result.append(res)
    return result


def random_no2():
    head = "22118800"
    result = []
    first = [0, 3, 5, 6, 8, 9]
    second = [0, 2, 3, 5, 6, 8, 9]
    last = [1, 2, 4, 5, 7, 9]
    for i in first:
        for j in second:
            for m in last:
                res = head + str(i) + "0" + str(j) + str(m)
                result.append(res)
    return result


if __name__ == '__main__':
    no2 = set(random_no2())
    no1 = set(random_no1())
    print(list(no1.difference(no2)))
