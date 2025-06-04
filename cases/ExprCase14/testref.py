def func(x,y):
    a=x in y
    return a

def func2(x,y):
    c=x not in y
    return c

print(func(1,[1,2,3]))
print(func(4,[1,2,3]))
print(func2(1,[1,2,3]))
print(func2(4,[1,2,3]))