import ast
from vizzy_api import activation_groups
from ..xml_gen import (
    Element,
    BinaryOp,
    BoolOp,
    Comparison,
    Constant,
    If,
    Not,
    SetActivationGroup,
    Variable,
    SetVariable,
    Vector,
)


def match_statement(stmt: ast.stmt):
    match stmt:
        case ast.Assign():
            return match_assign(stmt)
        case ast.AugAssign():
            return match_aug_assign(stmt)
        case ast.If(test=test, body=body):
            return match_if(test, body)
        case _:
            raise SyntaxError(f"Unexpected syntax:\n{ast.unparse(stmt)}")


def match_if(test: ast.expr, body: list[ast.stmt]):
    return If(match_expr(test), [match_statement(s) for s in body])


def match_assign(node: ast.Assign) -> Element:
    match node.targets, node.value:
        case [ast.Name(id=ag)], val if ag in activation_groups.__all__:
            ag = int(ag.lstrip("AG"))
            return SetActivationGroup(ag, match_expr(val))

        case [ast.Attribute(value=ast.Name(id="VAR"), attr=target)], expr:
            return SetVariable(target, match_expr(expr))

        case [ast.Name(id=name)], expr:
            return SetVariable(name, match_expr(expr), is_local=True)

        case _:
            raise SyntaxError(f"Unexpected assignment syntax:\n{ast.unparse(node)}")


def match_aug_assign(node: ast.AugAssign) -> Element:
    match node.target, node.op, node.value:
        case ast.Attribute(value=ast.Name(id="VAR")) as target, op, expr:
            return match_assign(ast.Assign([target], ast.BinOp(target, op, expr)))

        case ast.Name() as var, op, expr:
            return match_assign(ast.Assign([var], ast.BinOp(var, op, expr)))

        case _:
            raise SyntaxError(f"Unexpected assignment syntax:\n{ast.unparse(node)}")


def match_expr(expr: ast.expr) -> Element:
    match expr:
        case ast.Attribute(value=ast.Name(id="VAR"), attr=name):
            return Variable(name)

        case ast.Name(id=name):
            return Variable(name, is_local=True)

        case ast.Call(func=ast.Name(id="Vec"), args=[x, y, z]):
            return Vector(match_expr(x), match_expr(y), match_expr(z))

        case ast.Constant(value=val) if isinstance(val, bool):
            return Constant.from_bool(val)

        case ast.Constant(value=val) if isinstance(val, (int, float)):
            return Constant.from_number(val)

        case ast.Constant(value=val) if isinstance(val, str):
            return Constant.from_text(val)

        case ast.BinOp(left=left, op=op, right=right):
            return match_binary_op(left, op, right)

        case ast.Compare(left=left, ops=[op], comparators=[right]):
            return match_comparison(left, op, right)

        case ast.BoolOp(op=op, values=values):
            return match_bool_ops(op, values)

        case _:
            raise SyntaxError(f"Unexpected expression syntax:\n{ast.unparse(expr)}")


def match_binary_op(left: ast.expr, op: ast.operator, right: ast.expr) -> Element:
    operands = (match_expr(left), match_expr(right))
    match op:
        case ast.Add():
            return BinaryOp.add(*operands)
        case ast.Sub():
            return BinaryOp.sub(*operands)
        case ast.Mult():
            return BinaryOp.mul(*operands)
        case ast.Div():
            return BinaryOp.div(*operands)
        case ast.Mod():
            return BinaryOp.mod(*operands)
        case _:
            raise SyntaxError(f"Unsupported operation:\n{ast.unparse(op)}")


def match_comparison(left: ast.expr, op: ast.cmpop, right: ast.expr):
    operands = (match_expr(left), match_expr(right))
    match op:
        case ast.Lt():
            return Comparison.lt(*operands)
        case ast.LtE():
            return Comparison.lte(*operands)
        case ast.Gt():
            return Comparison.gt(*operands)
        case ast.GtE():
            return Comparison.gte(*operands)
        case ast.Eq():
            return Comparison.eq(*operands)
        case ast.NotEq():
            return Not(Comparison.eq(*operands))
        case _:
            raise SyntaxError(f"Unsupported operation:\n{ast.unparse(op)}")


def match_bool_ops(op: ast.boolop, values: list[ast.expr]):
    def get_func():
        match op:
            case ast.Or():
                return BoolOp.or_
            case ast.And():
                return BoolOp.and_
            case _:
                raise SyntaxError(f"Unsupported operation:\n{ast.unparse(op)}")

    fn = get_func()

    first = values.pop(0)
    next = values.pop(0)

    acc = fn(match_expr(first), match_expr(next))
    while len(values) > 0:
        next = values.pop(0)
        acc = fn(acc, match_expr(next))

    return acc
