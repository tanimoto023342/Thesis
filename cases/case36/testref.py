#ブラケット構文に問題あり→ブラケット構文に対する単一化は行わない、でいいかも
def copy(list1):
    list2=[0,0,0,0]
    for i in list1:
        list2[i]=i
    return list2

print(copy([1,2,3,4]))