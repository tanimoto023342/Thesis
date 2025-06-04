#ブラケット構文に問題あり→ブラケット構文に対する単一化は行わない、でいいかも
def sum(num):
    sum=num
    sum+=1
    return sum

print(sum(0))