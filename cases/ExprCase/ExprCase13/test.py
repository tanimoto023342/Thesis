#関数本文の文法は代入文と、exprの中でcompare_op_bitwise_or_pairまででカバーされているすべての式
a=2&3 is 2&3
print(a)

b=4^2 is 2&3
print(b)

c=2&3 is not 2&3
print(c)

d=4^2 is not 2&3
print(d)