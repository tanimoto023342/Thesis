def func():
    sum=0
    for i in [1,2,3]:
        for j in range(3):
            sum+=i
    else:
        print("for finished")

    return sum

print(func())