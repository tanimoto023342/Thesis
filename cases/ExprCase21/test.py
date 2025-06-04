#関数本文の文法は代入文と、expressionでカバーされているすべての式
a=3 if 3>2 else 2
print(a)

a=3 if 3+2 else 2
print(a)

a=3 if 3 is 2 else 2
print(a)

a=3 if 3 not in [1,2,3] else 2
print(a)