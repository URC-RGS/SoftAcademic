# [print(i**3) for i in range(1, round(float(input())) + 1)]

# s = 'Into each life some rain must fall, but too much is falling in mine..'
# check = True
# for i in s.split():
#     if check:
#         print(i.upper(), end=' ')
#     else:
#         print(i.lower(), end=' ')
#     check = not check

from functools import lru_cache


@lru_cache()
def factorial(n):
    if n == 0:
        return 1
    return factorial(n-1)*n


print(factorial(int(input())))
