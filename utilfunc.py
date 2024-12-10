import logging
import inspect
from myclass import UnDefined

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
