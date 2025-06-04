def func(expr):
    a=3 if expr else 2
    return a

print(func(3>2))
print(func(3+2))
print(func(3 is 2))
print(func(3 not in [1,2,3]))