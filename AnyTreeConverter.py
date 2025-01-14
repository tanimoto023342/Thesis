import logging
import ast
from anytree import AnyNode
from utilfunc import func_log
from myclass import UnDefined

@func_log
def ast_to_any_node(ast_node): #astNodeが引数
    """簡素化もここで行う"""
    field_value_dict=vars(ast_node)
    any_node=AnyNode(classname=type(ast_node).__name__,
                        name=UnDefined(),
                        id=UnDefined(),
                        value=UnDefined(),
                        func=UnDefined(),
                        arg=UnDefined(),
                        _NodeMixin__children=[],
                        )
    for i in field_value_dict:
        if i in any_node.__dict__.keys():
            if isinstance(field_value_dict[i], ast.AST):
                continue
            any_node.__dict__.update({i:field_value_dict[i]})#属性追加(AST_でanytreeの元々の属性と区別)
    logging.debug(f"ast_to_anytree_node return \n{any_node}\n")
    return any_node

@func_log
def convert_ast_to_anytree(ast_node,parent=None):
    any_node = ast_to_any_node(ast_node)#ここでノード生成されてる
    any_node.parent=parent

    for _, field_value in ast.iter_fields(ast_node):
        if isinstance(field_value, ast.AST):
            convert_ast_to_anytree(field_value,parent=any_node)
        elif isinstance(field_value, list):
            for item_in_list in field_value:
                if isinstance(item_in_list, ast.AST):
                    convert_ast_to_anytree(item_in_list, parent=any_node)
        else:
            pass
    logging.debug(f"convert_ast_to_anytree return \n{any_node}\n")
    return any_node