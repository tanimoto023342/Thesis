def func():
    a=True or True
    return a

def func1():
    b=True or False
    return b

def func2():
    c=False or True
    return c

def func3():
    d=False or False
    return d

print(func())
print(func1())
print(func2())
print(func3())