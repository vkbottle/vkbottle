import ast
import random
import string
from typing import Callable, Iterable

from typing_extensions import Protocol

from .base_converter import Converter, ConverterError

CALL_REPLACEMENTS = {
    "append": "push",
    "pop": "pop",
}
CALL_STRING = ["join", "strip", "split"]

converter = Converter()
find = converter.find_definition


def dispatch_keywords(keywords: Iterable, assigner: str = ":", sep: str = ","):
    return sep.join(f"{param.arg}{assigner}{find(param.value)}" for param in keywords)


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0].lower() + "".join(x.title() for x in components[1:])


@converter(ast.Assign)
def assign(d: ast.Assign):
    left = d.targets
    left_ = [find(target) for target in left if target.__class__ == ast.Name]
    right = find(d.value)
    return "var " + ",".join(f"{target}={right}" for target in left_) + ";"


@converter(ast.Add)
@converter(ast.UAdd)
def add_operator(_: ast.Add):
    return "+"


@converter(ast.Sub)
@converter(ast.USub)
def sub_operator(_: ast.Sub):
    return "-"


@converter(ast.Mult)
def mult_operator(_: ast.Mult):
    return "*"


@converter(ast.Div)
def div_operator(_: ast.Div):
    return "/"


@converter(ast.Pow)
def pow_operator(_: ast.Pow):
    return "**"


@converter(ast.RShift)
def rshift_operator(_: ast.RShift):
    return ">>"


@converter(ast.LShift)
def lshift_operator(_: ast.LShift):
    return "<<"


@converter(ast.BitAnd)
def bitand_operator(_: ast.BitAnd):
    return "&"


@converter(ast.BitOr)
def bitor_operator(_: ast.BitOr):
    return "|"


@converter(ast.Mod)
def mod_operator(_: ast.Mod):
    return "%"


@converter(ast.Gt)
def gt_operator(_: ast.Gt):
    return ">"


@converter(ast.Lt)
def lt_operator(_: ast.Lt):
    return "<"


@converter(ast.GtE)
def gt_operator_1(_: ast.GtE):
    return ">="


@converter(ast.LtE)
def gt_operator_2(_: ast.LtE):
    return "<="


@converter(ast.Eq)
def gt_operator_3(_: ast.Eq):
    return "=="


@converter(ast.NotEq)
def gt_operator_4(_: ast.Gt):
    return "!="


@converter(ast.And)
def and_operator(_: ast.And):
    return "&&"


@converter(ast.Or)
def or_operator(_: ast.Or):
    return "||"


@converter(ast.AugAssign)
def aug_assign(d: ast.AugAssign):
    operator = find(d.op)
    value = find(d.value)
    target = find(d.target)
    return f"{target} = {target} {operator} {value};"


@converter(ast.Constant)
def constant(d: ast.Constant):
    return d.value


@converter(ast.Name)
def name(d: ast.Name):
    return d.id


@converter(ast.While)
def while_cycle(d: ast.While):
    if d.orelse:
        raise ConverterError("You can't use while or/else in vkscript")
    body = "".join(find(line) for line in d.body)
    return "while(" + find(d.test) + "){" + body + "};"


@converter(ast.For)
def for_cycle(d: ast.For):
    random_iter_name = f"__iter_{random_string(5)}__"
    body = "".join(find(line) for line in d.body)
    return (
        f"var {random_iter_name} = {find(d.iter)};"
        f"while({random_iter_name}.length > 0){{var {find(d.target)}={random_iter_name}.pop();{body}}};"
    )


@converter(ast.If)
def if_statement(d: ast.If):
    return (
        "if("
        + find(d.test)
        + "){"
        + "".join(find(li) for li in d.body)
        + "}else{"
        + ("".join(find(e) for e in d.orelse) if len(d.orelse) else "")
        + "};"
    )


@converter(ast.Call)
def call(d: ast.Call):
    func: ast.Attribute = d.func  # type: ignore
    calls = []

    while isinstance(func, ast.Attribute):
        calls.append(func.attr)
        func = func.value  # type: ignore
    if func.__class__ == ast.Str:
        if calls[0] in CALL_STRING:
            return str(find(d.args[0])) + "." + calls[0] + "(" + find(func) + ")"
        elif calls[0] == "format":
            raise ConverterError("Use f-strings instead of str.format")
        raise ConverterError("String formatter")

    if func.id.lower() == "api":
        params = dispatch_keywords(d.keywords)
        return "API." + ".".join(map(to_camel_case, calls[::-1])) + "({" + params + "})"
    elif func.id == "len":
        return f"{find(d.args[0])}.length"
    elif calls and calls[0] in CALL_REPLACEMENTS:
        args = ",".join(find(arg) for arg in d.args)
        return find(d.func.value) + "." + CALL_REPLACEMENTS[calls[0]] + "(" + args + ")"  # type: ignore
    elif calls[0] in CALL_STRING:
        return find(func) + "." + calls[0] + "(" + find(d.args[0]) + ")"
    raise ConverterError(f"Call for {getattr(d.func, 'attr', d.func.__dict__)} is not referenced")


@converter(ast.Pass)
def pass_expr(_: ast.Pass):
    return ""


@converter(ast.Expr)
def expr(d: ast.Expr):
    return find(d.value) + ";"


@converter(ast.Module)
def module(d: ast.Module):
    return find(d.body)


@converter(ast.BinOp)
def bin_operation(d: ast.BinOp):
    return f"{find(d.left)}{find(d.op)}{find(d.right)}"


@converter(ast.Compare)
def compare(d: ast.Compare):
    left = find(d.left)
    operations = [
        f"{left}{find(operator)}{find(comparator)}"
        for operator, comparator in zip(d.ops, d.comparators)
    ]
    return "&&".join(operations)


@converter(ast.BoolOp)
def bool_op(d: ast.BoolOp):
    return find(d.op).join(find(value) for value in d.values)


@converter(ast.UnaryOp)
def unary_op(d: ast.UnaryOp):
    return f"{find(d.op)}{find(d.operand)}"


@converter(ast.Subscript)
def subscript(d: ast.Subscript):
    value = find(d.value)
    if d.slice.__class__ == ast.Index:
        if d.slice.value.__class__ == str:  # type: ignore
            return f"{value}.{d.slice.value.s}"  # type: ignore
        return f"{value}[{find(d.slice.value)}]"  # type: ignore
    raise ConverterError(f"Slice {d.slice} is not referenced")


@converter(ast.Attribute)
def attribute(d: ast.Attribute):
    return f"{find(d.value)}.{d.attr}"


@converter(ast.Return)
def return_statement(d: ast.Return):
    value = "null" if d is None else find(d.value)
    return f"return {value};"


@converter(ast.Delete)
def delete_statement(d: ast.Delete):
    return "".join(f"delete {find(target)};" for target in d.targets)


@converter(ast.Dict)
def dict_type(d: ast.Dict):
    dict_s = ",".join(f"{find(key)}:{find(value)}" for key, value in zip(d.keys, d.values))
    return "{" + dict_s + "}"


@converter(ast.Num)
def num_type(d: ast.Num):
    return str(d.n)


@converter(ast.Str)
def str_type(d: ast.Num):
    return repr(d.s)


@converter(ast.JoinedStr)
def joined_str(d: ast.JoinedStr):
    return "+".join(find(value) for value in d.values)


@converter(ast.FormattedValue)
def formatted_value(d: ast.FormattedValue):
    return find(d.value)


@converter(ast.List)
@converter(ast.Tuple)
def list_type(d: ast.List):
    return "[" + ",".join(find(a) for a in d.elts) + "]"


@converter(ast.NameConstant)
def name_constant_type(d: ast.NameConstant):
    consts = {True: "true", False: "false", None: "null"}
    return consts[d.value]


class VKScriptFunction(Protocol):
    def __call__(self, **kwargs) -> str:
        ...


def vkscript(func: Callable) -> VKScriptFunction:
    def decorator(**context):
        return converter.scriptify(func, **context)

    return decorator
