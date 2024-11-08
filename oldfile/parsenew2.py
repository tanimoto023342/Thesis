import ast
from anytree import Node, RenderTree
import sys
from anytree.exporter import UniqueDotExporter
import graphviz

def func_for_name(node):
    field_value_dict=vars(node)
    name = f"type1→{type(node).__name__}\n"
    if 'value' in field_value_dict:
        objvalue=field_value_dict['value']
        typename=type(field_value_dict['value']).__name__
        if typename=="Call" or typename=="Name": #オブジェクトアドレス表示回避
            name+=f"value→<ASTobject>(objtype→{typename})"
        else:
            name+=f"value→{objvalue}(objtype→{typename})"
    if 'func' in field_value_dict:
        name+=f"type2→func"
    if 'id' in field_value_dict:
        name+=f"id→{field_value_dict['id']}"
    if 'arg' in field_value_dict:
        name+=f"id→{field_value_dict['arg']}"
    return name

# ASTノードをanytreeノードに変換する関数
def convert_ast_to_anytree(ast_node,parent=None):
    node_name = func_for_name(ast_node)
    node = Node(node_name, parent=parent)
    for field, value in ast.iter_fields(ast_node):
        if isinstance(value, ast.AST):
            convert_ast_to_anytree(value,parent=node)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    convert_ast_to_anytree(item, parent=node)
    return node

def compare_nodes(node1,node2,treelist1=[],treelist2=[]):
    print(0)
    if node1.parent!=None and node2.parent!=None:    
        len1=len(node1.parent.children)
        len2=len(node2.parent.children)
        print(node1.parent.children)     
    iter1=iter(node1.children)
    iter2=iter(node2.children)   
    print(node1.name+"\n#"+node2.name+'\n')                                                                                                                                                                                      
    if(node1.name==node2.name):
        print(1)
        n1=next(iter1)
        n2=next(iter2)
        while(True):
            try:
                treelist1,treelist2=compare_nodes(n1,n2,treelist1,treelist2)
                if treelist1!=[] and treelist1[-1]==n1:
                    n1=next(iter1)
                elif treelist2!=[] and treelist2[-1]==n2:
                    n2=next(iter2)
                else: 
                    n1=next(iter1)
                    n2=next(iter2)
            except StopIteration:
                if n1==node1.children[-1]:
                    pass
                else:
                    try:
                        while(True):
                            treelist1.append(n1)
                            n1=next(iter1)
                    except StopIteration:
                        pass
                if n2==node2.children[-1]:
                    pass
                else:
                    try:
                        while(True):
                            treelist2.append(n2)
                            n2=next(iter2)
                    except StopIteration:
                        pass
                break
        #for n1,n2 in zip(node1.children,node2.children):
            #treelist1,treelist2=compare_nodes(n1,n2,treelist1,treelist2)
    else:
        print(2)
        if len1>len2:
            node1.parent=None
            treelist1.append(node1)
        else:
            node2.parent=None
            treelist2.append(node2)
    return treelist1,treelist2

if len(sys.argv) > 2:
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
else:
    print("not enough argument")
    exit(0)

f1=open(filename1, encoding="utf-8")
parsed_ast1 = ast.parse(f1.read())

f2=open(filename2, encoding="utf-8")
parsed_ast2 = ast.parse(f2.read())

tree1=convert_ast_to_anytree(parsed_ast1)
tree2=convert_ast_to_anytree(parsed_ast2)

dot1 = graphviz.Digraph(comment='Forest')
dot2 = graphviz.Digraph(comment='Forest')

UniqueDotExporter(tree1).to_picture("tree.png")

list1,list2=compare_nodes(tree1,tree2)
print(list1)
print(list2)

treeid=0
for t in list1:
    c=0
    for i in t.descendants:
        i.name+='\n'+str(c)
        c+=1
    for pre, fill, node in RenderTree(t):
        dot1.node(f"treeid={treeid}\n"+node.name)
        if node.parent:
            dot1.edge(f"treeid={treeid}\n"+node.parent.name, f"treeid={treeid}\n"+node.name)
    treeid+=1

for t in list2:
    c=0
    for i in t.descendants:
        i.name+='\n'+str(c)
        c+=1
    for pre, fill, node in RenderTree(t):
        dot2.node(f"treeid={treeid}\n"+node.name)
        if node.parent:
            dot2.edge(f"treeid={treeid}\n"+node.parent.name, f"treeid={treeid}\n"+node.name)
    treeid+=1

# ツリーを表示
UniqueDotExporter(tree1).to_picture("cotree.png")

dot1.render('forest1', format='png', cleanup=True)
dot2.render('forest2', format='png', cleanup=True)