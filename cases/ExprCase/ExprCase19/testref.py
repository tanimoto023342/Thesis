def func():
    a=True and True
    return a

def func1():
    b=True and False
    return b

def func2():
    c=False and True
    return c

def func3():
    d=False and False
    return d

print(func())
print(func1())
print(func2())
print(func3())