import ast
from anytree import AnyNode, search
import sys
from anytree.exporter import UniqueDotExporter
import logging
import copy

logging.basicConfig(filename="judgeprog.log", level=logging.DEBUG, filemode='w')

#今回の判定で使う最低限の属性
attrWhitelist=["value","func","id","arg","name"]

class UnDefined:
    __instance=None

    def __new__(cls): #たった１つのインスタンスのアドレスと同値であることをもって未定義を定義するクラス
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

        
    def __repr__(self):
        return "UnDefined"
    
    def __str__(self):
        return "UnDefined"
    
    def __eq__(self, other):
        if isinstance(other, UnDefined):
            return True
        else:
            False

def copy_tree(node):
    """先通り順でcopy 親子関係はcopyしない"""
    cnode=AnyNode()
    for i in vars(node):
        if (i=="_NodeMixin__children" or
            i=="_NodeMixin__parent"):
                continue
        cnode.__dict__.update({i:node.__dict__[i]})
    for t in node.children:
        node1=copy_tree(t)
        node1.parent=cnode
    return cnode


def insert_child(parentNode, num, nodelist=[]):
    """
    parentNode=子どもの挿入を行いたいノード
    num=子どもを挿入したい位置
    nodelist=挿入したいノードのリスト
    """
    stack=[]
    childlen=len(parentNode.children)
    for i in range(childlen-num):
        target=parentNode.children[childlen-1-i]
        target.parent=None
        stack.append(target)
    for i in nodelist:
        node=copy_tree(i)
        node.parent=parentNode
    for _ in range(len(stack)):
        j=stack.pop()
        j.parent=parentNode

def ast_to_anytree_node(astNode): #astNodeが引数
    """簡素化もここで行う"""
    logging.debug(f"ast_to_anytree_node(astNode={astNode})\n")
    field_value_dict=vars(astNode)
    anytreeNode=AnyNode(classname=type(astNode).__name__,
                        name=UnDefined(),
                        id=UnDefined(),
                        value=UnDefined(),
                        func=UnDefined(),
                        arg=UnDefined(),
                        _NodeMixin__children=[],
                        )
    for i in field_value_dict:
        if i in anytreeNode.__dict__.keys():
            if isinstance(field_value_dict[i], ast.AST):
                continue
            anytreeNode.__dict__.update({i:field_value_dict[i]})#属性追加(AST_でanytreeの元々の属性と区別)
    logging.debug(f"ast_to_anytree_node return \n{anytreeNode}\n")
    return anytreeNode

# ASTノードをanytreeノードに変換する関数
def convert_ast_to_anytree(ast_node,parent=None):
    logging.debug(f"convert_ast_to_anytree\n(ast_node={ast_node},\nparent={parent})\n")
    node = ast_to_anytree_node(ast_node)#ここでノード生成されてる
    node.parent=parent

    for _, value in ast.iter_fields(ast_node):
        if isinstance(value, ast.AST):
            convert_ast_to_anytree(value,parent=node)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    convert_ast_to_anytree(item, parent=node)
        else:
            pass
    logging.debug(f"convert_ast_to_anytree return \n{node}\n")
    return node

def compare_nodes(node1,node2):
    logging.debug(f"compare_nodes\n(node1={node1}, \nnode2={node2})\n")
    # ノードの要素が一致しているか確認
    if len(node1.__dict__) == len(node2.__dict__):
        c1=node1.__dict__
        c2=node2.__dict__
        for i,j in zip(c1,c2):#辞書の各要素(=ノードの変数)が一致しているか確認
            if (i=="_NodeMixin__children" or
                j=="_NodeMixin__children" or
                i=="_NodeMixin__parent" or
                j=="_NodeMixin__parent" ):
                continue
            if i!=j or c1[i]!=c2[j]:
                logging.debug(f"compare_nodes retun False\npair:{c1}\n{c2}\n")
                return False
    else:
        logging.debug(f"compare_nodes return False\nlen:{len(node1.__dict__)} {len(node2.__dict__)}\n{node1.__dict__}\n{node2.__dict__}\n")
        return False
    
    
    # 子ノードの数が一致しているか確認
    if len(node1.children) != len(node2.children):
        logging.debug(f"compare_nodes return False\n")
        return False

    # 子ノードをそれぞれ比較（再帰的に）
    for child1, child2 in zip(node1.children, node2.children):
        if not compare_nodes(child1, child2):
            logging.debug(f"compare_nodes return False\n")
            return False
    
    # すべて一致していればTrueを返す
    logging.debug(f"compare_nodes return True\n")
    return True

def check_new_func(node1,node2):#node2がnewfuncを持つと仮定
    logging.debug(f"checkNewfunc\n({node1},{node2})\n")
    if node2.classname=="FunctionDef":
        return node2
    result1=False
    for i in node2.children: #funcdefじゃなかったら他のノードを探索
        if node2.children!=[]:
            result1=check_new_func(node1,i)
        if result1: #ノードが見つかったら探索打ち切り
            result2=search.find(node1, lambda node: node.name == result1.name)#名前が一致する関数がもう１つの木にないか探索
            if result2: 
                continue
            else:
                break#もし一致するFunctionDefはもう１つの木になければその関数が新しいものと判定
    return result1
        
def check_func_call(name,node,callList=[]):
    """
    name:新たに定義された関数の名前
    node:探索対象ノード
    """
    logging.debug(f"checkFuncCall\n({name},{node})\n")
    if node.classname=="Call":
        for i in node.children:
            if i.id == name:
                callList.append(node)
                return callList
    else:
        for i in node.children: #再帰探索
            callnode=check_func_call(name,i)
    return callList

def check_func_body(body,node):#tryerror付加予定
    logging.debug(f"checkFuncbody\n({body},{node})\n")
    flag=0
    for i in node.children:
        if compare_nodes(i,body[0]):
            body.pop(0)
            flag=1
            if body==[]:
                return True
        else:
            if flag==1:
                return False
    return False

def check_and_modify_extract(t1,t2):
    logging.debug(f"checkExtract\n({t1},{t2})\n")
    newfuncnode=check_new_func(t1,t2) #新たに定義された関数の定義木を代入
    if not newfuncnode:
        return False
    calltreeList=check_func_call(newfuncnode.name,t2)
    logging.info(f"calltreeList=\n{calltreeList}\n")
    if calltreeList==[]: #新たに定義された関数の定義を発見
        return False
    
    #関数のボディを抽出する処理
    body=[]
    for i in newfuncnode.children:
        if i.classname!="arguments":
            body.append(i)

    temp=copy.deepcopy(body)

    bodytree=check_func_body(temp,t1)

    if not bodytree:
        return False#上で発見した関数のボディを削除された部分木の中から発見

    newfuncnode.parent=None
    for n in calltreeList:
        exprnode=n.parent#呼び出しを示す文の木の先頭となるexprノードを取得
        temp=exprnode.parent
        insertNum=temp.children.index(exprnode)
        exprnode.parent=None
        insert_child(temp, insertNum, body)

    return True

def attr_writer(node):
    text_in_label=""
    node_attr=vars(node)

    for i in node_attr:
        if (i=="_NodeMixin__children" or
            i=="_NodeMixin__parent"):
            continue
        if node_attr[i] is not UnDefined():
            text_in_label+=f"{i}:{node_attr[i]}\n"

    return 'label=\"'+text_in_label+'\"'

def main():
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

    logging.info("start making AST1 to anytree\n")
    tree1=convert_ast_to_anytree(parsed_ast1)
    logging.info("start making AST2 to anytree\n")
    tree2=convert_ast_to_anytree(parsed_ast2)
    logging.info("finished making anytree\n")

    UniqueDotExporter(tree1).to_picture("tree.png")

    logging.info("start comparing tree\n")
    itti=compare_nodes(tree1,tree2)
    logging.info("finished comparing tree\n")
    logging.info(f"compare_nodes({tree1.classname},{tree2.classname})\n={itti}\n")

    if itti == True:
        print("Exact Match",end='')
        return
    else:
        pass

    # ツリーを表示
    UniqueDotExporter(tree1, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree1.png")
    UniqueDotExporter(tree2, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree2.png")

    logging.info("start checking Extract\n")
    tf=check_and_modify_extract(tree1,tree2)
    logging.info("finished checking Extract\n")
    logging.info(f"checkExtract({tree1.classname},{tree2.classname})\n={tf}\n")

    UniqueDotExporter(tree1, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree1after.png")
    UniqueDotExporter(tree2, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree2after.png")
    if tf and compare_nodes(tree1,tree2):
        print("Stractual Match",end='')
    else:
        print("No Match",end='')

    return

logging.info("program started\n")
main()
logging.info("program finished\n")