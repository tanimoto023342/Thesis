#ブラケット構文に問題あり→ブラケット構文に対する単一化は行わない、でいいかも
def sum(num):
    sum=num
    for _ in range(3):  
        sum+=1
    return sum

print(sum(0))