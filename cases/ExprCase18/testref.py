def func(x,y):
    a=not x == y
    return a

def func2(x,y):
    c=not x != y
    return c

print(func(1,4))
print(func2(1,4))
print(func(1,1))
print(func2(1,1))