cases=case1 case2 case3 case4 case5 case6 case7 \
case8 case9 case10 case11 case12 case13 case14 \
case15 case16 case17 case18 case19 case20 case21 case22 case23\
case24

main:
	for case in $(cases);do \
	prog=$$case/test.py; \
	progref=$$case/testref.py; \
    exp=$$case/exp.txt; \
    echo $$case; \
	python judgeprog.py $$prog $$progref > $$case/out.txt; \
	diff -B -w $$case/out.txt $$exp; \
	done

unit:
	python judgeprog.py test.py testref.py
