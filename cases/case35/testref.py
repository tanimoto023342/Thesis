def copy(list):
    list2=[0,0,0,0]
    for i in range(4):
        list2[i]=list[i]
    return list2

list=[1,2,3,4]
print(copy(list))