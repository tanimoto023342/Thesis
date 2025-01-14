import ast
import sys
from myclass import UnDefined

def attr_writer(node):
    text_in_label=""
    node_attr=vars(node)

    for i in node_attr:
        if ((i=="_NodeMixin__children") |
            (i=="_NodeMixin__parent")):
            continue
        if node_attr[i] is not UnDefined():
            text_in_label+=f"{i}:{node_attr[i]}\n"

    return 'label=\"'+text_in_label+'\"'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemError("ソースファイル名を指定してください")
    
    filename=sys.argv[1]

    with open(filename,encoding="utf-8") as f:
        f_content=f.read()
        parsed_ast=ast.parse(f_content)
    

