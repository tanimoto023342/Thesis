def func(x,y):
    a=x is y
    return a

def func2(x,y):
    c=x is not y
    return c

print(func(2&3,2&3))
print(func(4^2, 2&3))
print(func2(2&3,2&3))
print(func2(4^2,2&3))