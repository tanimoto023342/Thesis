list=[0]

sum=0
for i in list:
    sum+=i

print(sum)

list.append(1)

sum=0
for i in list:
    sum+=i

print(sum)
list=list+[2,3]

sum=0
for i in list:
    sum+=i

print(sum)