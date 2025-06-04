#関数本文の文法は代入文と、exprの中でdisjunctionまででカバーされているすべての式
a=True or True
print(a)

b=True or False
print(b)

c=False or True
print(c)

d=False or False
print(d)