#ブラケット構文に問題あり→ブラケット構文に対する単一化は行わない、でいいかも
def func():
    a=0
    return a

print(func())