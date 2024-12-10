import ast
import sys
import logging
import copy
from anytree import AnyNode, search
from anytree.exporter import UniqueDotExporter
import inspect

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
    
    def __is__(self, other):
        if isinstance(other, UnDefined):
            return True
        else:
            return False

class container_for_func_info:
    def __init__(self,body_tree_list=[],return_tree=None):
        self.body_tree_list=body_tree_list
        self.return_tree=return_tree

    def __repr__(self):
        return f"(body_tree_list:{self.body_tree_list},return_tree:{self.return_tree})"

class func_info:
    def __init__(self,FuncDef_node):
        self.FuncDef_node=FuncDef_node
        self.call_list=[]
        self.arguments_dict={}
        self.body_tree_list=[]
        self.return_tree=None
        self.func_tree_dict={}

    def append_call(self,call_node):
        self.call_list.append(call_node)

    def arguments_dict_init(self):
        for i in self.call_list:
            self.arguments_dict.setdefault(i,[])

    def append_arguments_in_dict(self,call_node,*arguments):
        try:
            self.arguments_dict[call_node].appned(arguments)
        except:
            logging.critical("exception happened\n")
            self.arguments_dict.setdefault(call_node,[arguments])

    def func_tree_dict_init(self):
        for i in self.call_list:
            self.func_tree_dict.setdefault(i,container_for_func_info())

    def func_tree_dict_update(self,key,/,body_tree_list=None,return_tree=None):
        if (body_tree_list is None) & (return_tree is None):
            logging.warning("辞書を更新する要素が与えられていません")
            return
        else:
            self.func_tree_dict.setdefault(key,container_for_func_info(body_tree_list,return_tree))

    def __repr__(self):
        return f"func_info({self.FuncDef_node})"            
    
    def show_all_info(self,/,mode="print"):
        if mode=="print":
            print(f"""FuncDef_node={self.FuncDef_node}
                  call_list={self.call_list}
                    arguments_dict={self.arguments_dict}
                    body_tree_list={self.body_tree_list}
                    return_tree={self.return_tree}
                    func_tree_dict=\n\t\t{self.func_tree_dict}""")
        elif mode=="debug":
            pass
        else:
            raise SyntaxError("不明なmodeです")

def custom_repr(self, args=None, nameblacklist=None):
    classname = self.__class__.__name__
    args = args or []
    nameblacklist = nameblacklist or []
    for key, value in filter(
        lambda item: not item[0].startswith("_") and item[0] not in nameblacklist and self.__dict__[item[0]] is not UnDefined(),
        sorted(self.__dict__.items(), key=lambda item: item[0]),
    ):
        args.append("%s=%r" % (key, value))
    return "%s(%s)" % (classname, ", ".join(args))

AnyNode.__repr__=custom_repr

def func_log(func):
    func_struct=inspect.signature(func)
    def inner(*args,**keywds):
        args_detail=""
        count=0
        args_tuple=args+tuple(keywds.values())
        for i in func_struct.parameters.values():
            try:
                if not (args_tuple[count] is UnDefined()):
                    args_detail+=f"{i}:{args_tuple[count]}, "
                else:
                    pass
            except:
                break
            count+=1
        logging.debug(f"{func.__name__}({args_detail})\n\n")
        result=func(*args,**keywds)
        return result
    return inner

@func_log
def copy_tree(node):
    """先通り順でcopy 親子関係はcopyしない"""
    if node is None:
        return None
    else:
        pass

    cnode=AnyNode()
    try:
        for i in vars(node):
            if ((i=="_NodeMixin__children") |
                (i=="_NodeMixin__parent")):
                    continue
            cnode.__dict__.update({i:node.__dict__[i]})
    except TypeError as e:
        print(f"{e}:vars() argument must have __dict__ attribute\n(node={node})")
        exit(1)
    for t in node.children:
        node1=copy_tree(t)
        node1.parent=cnode
    return cnode

@func_log
def insert_child(parentNode, num, nodelist=[]):
    """
    parentNode=子どもの挿入を行いたいノード\n
    num=子どもを挿入したい位置\n
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

@func_log
def ast_to_anytree_node(astNode): #astNodeが引数
    """簡素化もここで行う"""
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
@func_log
def convert_ast_to_anytree(ast_node,parent=None):
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

@func_log
def open_file_and_make_ast(filename1,filename2):
    with open(filename1, encoding="utf-8") as f1:
        f1_content=f1.read()
        parsed_ast1 = ast.parse(f1_content)

    with open(filename2, encoding="utf-8") as f2:
        f2_content=f2.read()
        parsed_ast2 = ast.parse(f2_content)

    logging.info("start making AST1 to anytree\n")
    tree1=convert_ast_to_anytree(parsed_ast1)
    logging.info("start making AST2 to anytree\n")
    tree2=convert_ast_to_anytree(parsed_ast2)
    logging.info("finished making anytree\n")

    return (tree1,tree2)

@func_log
def compare_nodes(node1,node2):
    # ノードの要素が一致しているか確認
    if len(node1.__dict__) == len(node2.__dict__):
        c1=node1.__dict__
        c2=node2.__dict__
        for i,j in zip(c1,c2):#辞書の各要素(=ノードの変数)が一致しているか確認
            if ((i=="_NodeMixin__children") |
                (j=="_NodeMixin__children") |
                (i=="_NodeMixin__parent") |
                (j=="_NodeMixin__parent") ):
                continue
            if (i!=j) | (c1[i]!=c2[j]):
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

@func_log
def check_new_func(node1,node2,func_info_dict={}):#node2がnewfuncを持つと仮定
    if node2.classname=="FunctionDef":
        search_result=search.find(node1, filter_=lambda node: node.name == node2.name)#名前が一致する関数がもう１つの木にないか探索
        if search_result:
            pass
        else:
            func_info_dict[node2.name]=func_info(node2)
            return func_info_dict
    
    for i in node2.children: #funcdefじゃなかったら他のノードを探索
        if node2.children!=[]:
            func_info_dict=check_new_func(node1,i,func_info_dict)

    return func_info_dict

@func_log   
def check_func_call(name_list,func_info_dict,node):
    """
    node:探索対象ノード
    """
    if node.classname=="Call":
        for i in node.children:
            for name in name_list:
                if i.id == name:
                    func_info_dict[name].call_list.append(node)
                    return func_info_dict
    else:
        pass
    for i in node.children: #再帰探索
        check_func_call(name_list,func_info_dict,i)
    return func_info_dict

@func_log
def check_func_body(body_list,tree_node):#tryerror付加予定
    flag=0
    iter_body=0
    delete_tree_list=[]
    for i in tree_node.children:
        if compare_nodes(i,body_list[iter_body]):
            iter_body+=1
            flag=1
            delete_tree_list.append(i)
            if iter_body==len(body_list):
                return True
        else:
            if flag==1:
                iter_body=0
                delete_tree_list.clear()
        if check_func_body(body_list,i): #真偽に関わらず再帰そのものは行う(↓の層を必ず確認したいため)
            return True
    return False

@func_log
def check_func_return(return_tree,tree_node):
    if tree_node is None:
        return False
    if search.findall(return_tree):
        pass
    else:
        return False     
    return True

@func_log
def modify_extract(func_info_dict):
    for func_info_ in func_info_dict.values():
        new_func_node=func_info_.FuncDef_node
        new_func_node.parent=None
        for n in func_info_.call_list:
            body_list=func_info_.func_tree_dict[n].body_tree_list
            if (n.parent.classname=="Expr") & (body_list is not None):
                exprnode=n.parent#呼び出しを示す文の木の先頭となるexprノードを取得
                temp=exprnode.parent
                insert_num=temp.children.index(exprnode)
                exprnode.parent=None
                insert_child(temp, insert_num,body_list)
            else:
                parent_node=n.parent
                insert_num=parent_node.children.index(n)
                insert_child(parent_node, insert_num, [func_info_.func_tree_dict[n].return_tree])
                node_in_Call=n
                while node_in_Call.parent.classname!="Module":
                    node_in_Call=node_in_Call.parent
                insert_num=node_in_Call.parent.children.index(node_in_Call)
                insert_child(node_in_Call.parent, insert_num, body_list) if body_list is not None else None
                n.parent=None

@func_log
def variable_unification(tree_root,variable_name,arg_node):
    #探索時該当する変数ノードをelementに置き換える
    if tree_root.id==variable_name:
        copied_arg_node=copy_tree(arg_node)
        insert_num=tree_root.parent.children.index(tree_root)
        insert_child(tree_root.parent,insert_num,[copied_arg_node])
        tree_root.parent=None
        result=copied_arg_node
    else:
        if tree_root.children:
            for t in tree_root.children:
                if tree_root.classname=="Subscript" and t==tree_root.children[0]:
                    continue #リストのブラケット構文に対する例外処理
                result=variable_unification(t,variable_name,arg_node)
        else:
            return tree_root
    return result

@func_log
def multiple_variable_unification(body_copy,variable_name_list,arg_node_list):
    if len(variable_name_list)!=len(arg_node_list):
        raise SystemError("仮引数と実引数の数が一致していません")
    else:
        if isinstance(body_copy, list) and body_copy:
            for tree_root in body_copy:
                for i,j in zip(variable_name_list,arg_node_list):
                    variable_unification(tree_root,i,j)
    return body_copy

@func_log
def check_extract(t1,t2):
    func_info_dict=check_new_func(t1,t2) #新たに定義された関数を発見し, 辞書に登録

    if func_info_dict=={}:
        return False
    else:
        pass

    func_info_dict=check_func_call(func_info_dict.keys(),func_info_dict,t2)
    
    logging.info(f"func_info_dict=\n{func_info_dict}\n")
    for i in func_info_dict.values():
        if i.call_list==[]: #新たに定義された関数の定義を発見
            pass
        else:
            break
    else:
        return False
    
    #関数のボディを抽出する処理
    body=[]
    return_tree=None
    variable_name_list=[]
    for func_info_ in func_info_dict.values():
        node=func_info_.FuncDef_node
        for i in node.children:
            if i.classname=="Return":
                return_tree=i.children[0]
            elif i.classname!="arguments":
                body.append(i)
            else:
                for j in i.children:
                    variable_name_list.append(j.arg)
        func_info_.body_tree_list=copy.deepcopy(body)
        func_info_.return_tree=copy.deepcopy(return_tree)

        for call_tree in func_info_.call_list:
            return_tree_copy=copy.deepcopy(return_tree)
            body_copy=copy.deepcopy(body)
            arg_node_list=[]
            for j in call_tree.children:
                print(j)
                if j.classname != "Name":
                    arg_node_list.append(j)
            body_copy=multiple_variable_unification(body_copy,variable_name_list,arg_node_list) if body_copy else None
            return_tree_copy=multiple_variable_unification(return_tree_copy,variable_name_list,arg_node_list)
            del arg_node_list
            func_info_.func_tree_dict_update(call_tree,body_tree_list=body_copy,return_tree=return_tree_copy)

        t1copy=copy.deepcopy(t1)
        bodytree=True
        for i in func_info_.call_list:
            if i.parent.classname=="Expr":
                body_list=func_info_.func_tree_dict[i].body_tree_list
                if body_list==[]:
                    continue
                else:
                    bodytree=check_func_body(body_list,t1copy)
            else:
                r_tree=func_info_.func_tree_dict[i].return_tree
                if r_tree is None:
                    return False
                bodytree=check_func_return(r_tree,t1copy)

        if not bodytree:
            return False#上で発見した関数のボディを削除された部分木の中から発見
        body.clear()

    return func_info_dict

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

def main():
    if len(sys.argv) >= 3:
        filename1 = sys.argv[1]
        filename2 = sys.argv[2]
    else:
        print("not enough argument")
        exit(0)

    tree1,tree2=open_file_and_make_ast(filename1,filename2)

    logging.info("start comparing tree\n")
    match_bool=compare_nodes(tree1,tree2)
    logging.info("finished comparing tree\n")
    logging.info(f"compare_nodes({tree1.classname},{tree2.classname})\n={match_bool}\n")

    if match_bool == True:
        print("Exact Match",end='')
        return
    else:
        pass

    # ツリーを表示
    UniqueDotExporter(tree1, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree1.png")
    UniqueDotExporter(tree2, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree2.png")

    logging.info("start checking Extract\n")
    extract_result=check_extract(tree1,tree2)
    logging.info("finished checking Extract\n")
    logging.info(f"checkExtract({tree1.classname},{tree2.classname})\n={extract_result}\n")

    if extract_result == False:
        print("No Match",end='')
        return
    
    #extract_result["func"].show_all_info()
    
    modify_extract(extract_result)

    UniqueDotExporter(tree1, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree1after.png")
    UniqueDotExporter(tree2, nodeattrfunc=lambda n: attr_writer(n)).to_picture("tree2after.png")

    modified_tree_match_bool=compare_nodes(tree1,tree2)

    if modified_tree_match_bool==True:
        print("Stractual Match",end='')
    else:
        print("No Match",end='')

    return

logging.info("program started\n")
main()
logging.info("program finished\n")