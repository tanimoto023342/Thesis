#関数本文の文法は代入文と、exprの中でinversionまででカバーされているすべての式
a=not 1 == 4
print(a)

b=not 1 != 4
print(b)

c=not 1 == 1
print(c)

d=not 1 != 1
print(d)