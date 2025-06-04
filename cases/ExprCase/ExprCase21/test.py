#関数本文の文法は代入文と、expressionでカバーされているすべての式
a=3 if 3>2 else 2
print(a)

b=3 if 3+2 else 2
print(b)

c=3 if 3 is 2 else 2
print(c)

d=3 if 3 not in [1,2,3] else 2
print(d)