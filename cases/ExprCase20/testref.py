def func(x,y):
    a=x or y
    return a

print(func(True,True))
print(func(True,False))
print(func(False,True))
print(func(False,False))