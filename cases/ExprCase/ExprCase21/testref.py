def func():
    a=3 if 3>2 else 2
    return a

def func1():
    b=3 if 3+2 else 2
    return b

def func2():
    c=3 if 3 is 2 else 2
    return c

def func3():
    d=3 if 3 not in [1,2,3] else 2
    return d

print(func())
print(func1())
print(func2())
print(func3())