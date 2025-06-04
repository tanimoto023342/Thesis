#関数本文の文法は代入文と、expressionでカバーされているすべての式
sum=0
for i in [1,2,3]:
    for j in range(3):
        sum+=i
else:
    print("for finished")

print(sum)

