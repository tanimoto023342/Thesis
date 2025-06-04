def func():
    a=not 1 == 4
    return a

def func1():
    b=not 1 != 4
    return b

def func2():
    c=not 1 == 1
    return c

def func3():
    d=not 1 != 1
    return d

print(func())
print(func1())
print(func2())
print(func3())