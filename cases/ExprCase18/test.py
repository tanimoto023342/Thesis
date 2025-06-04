#関数本文の文法は代入文と、exprの中でcompare_op_bitwise_or_pairまででカバーされているすべての式
a=not 1 == 4
print(a)

c=not 1 != 4
print(c)

a=not 1 == 1
print(a)

c=not 1 != 1
print(c)