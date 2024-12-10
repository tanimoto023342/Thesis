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