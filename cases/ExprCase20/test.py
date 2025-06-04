#関数本文の文法は代入文と、exprの中でconjunctionまででカバーされているすべての式
a=True or True
print(a)

a=True or False
print(a)

a=False or True
print(a)

a=False or False
print(a)