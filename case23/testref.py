def printListSum():
    sum=0
    for i in list:
        sum+=i

    print(sum)

list=[0]

printListSum()

list.append(1)

printListSum()

list=list+[2,3]

printListSum()