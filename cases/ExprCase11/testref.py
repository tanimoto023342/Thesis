def func(x,y):
    a=x&y
    return a

def func1(x,y):
    b=x^y
    return b

def func2(x,y,z):
    c=x&y^z
    return c

def func3(x,y,z):
    d=x<<y+z
    return d

print(func(2,3))
print(func1(4,2))
print(func2(5,2,2))
print(func3(5,2,3))