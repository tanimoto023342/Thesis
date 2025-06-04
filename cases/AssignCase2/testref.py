def func():
    a=1
    a|=0
    return a

def func1():
    b=0
    b^=1
    return b

def func2():
    c=0
    c<<=1
    return c

def func3():
    d=1
    d>>=2
    return d

def func4():
    e=6
    e**=3
    return e

def func5():
    f=6
    f//=3
    return f

print(func())
print(func1())
print(func2())
print(func3())
print(func4())
print(func5())