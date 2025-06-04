def func():
    a=1 in [1,2,3]
    return a

def func1():
    b=4 in [1,2,3]
    return b

def func2():
    c=1 not in [1,2,3]
    return c

def func3():
    d=4 not in [1,2,3]
    return d

print(func())
print(func1())
print(func2())
print(func3())