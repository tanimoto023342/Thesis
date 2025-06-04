def copy(list):
    list2=[0,0,0,0]
    for i in range(4):
        list2[i]=list[i]
    return list2

print(copy([1,2,3,4]))