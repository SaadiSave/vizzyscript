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
    ActivationGroup,
)


def match_statement(stmt: ast.stmt):
    match stmt:
        case ast.Assign():
            return match_assign(stmt)
        case ast.AugAssign():
            return match_aug_assign(stmt)
        case ast.If(test=test, body=body):
            return match_if(test, body)
        case ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="AG"), attr="set"),
                args=[ag, expr],
            )
        ):
            return SetActivationGroup(match_expr(ag), match_expr(expr))
        case _:
            raise SyntaxError(
                f"Unexpected syntax:\n{ast.unparse(stmt)}\n{ast.dump(stmt)}"
            )


def match_if(test: ast.expr, body: list[ast.stmt]):
    return If(match_expr(test), [match_statement(s) for s in body])


def match_assign(node: ast.Assign) -> Element:
    match node.targets, node.value:
        case [ast.Name(id=ag)], val if ag in activation_groups.__all__:
            ag = int(ag.lstrip("AG"))
            return SetActivationGroup(Constant.from_number(ag), match_expr(val))

        case [ast.Attribute(value=ast.Name(id="VAR"), attr=target)], expr:
            return SetVariable(target, match_expr(expr))

        case [ast.Name(id=name)], expr:
            return SetVariable(name, match_expr(expr), is_local=True)

        case _:
            raise SyntaxError(
                f"Unexpected assignment syntax:\n{ast.unparse(node)}\n{ast.dump(node)}"
            )


def match_aug_assign(node: ast.AugAssign) -> Element:
    match node.target, node.op, node.value:
        case ast.Attribute(value=ast.Name(id="VAR")) as target, op, expr:
            return match_assign(ast.Assign([target], ast.BinOp(target, op, expr)))

        case ast.Name() as var, op, expr:
            return match_assign(ast.Assign([var], ast.BinOp(var, op, expr)))

        case _:
            raise SyntaxError(
                f"Unexpected assignment syntax:\n{ast.unparse(node)}\n{ast.dump(node)}"
            )


def match_expr(expr: ast.expr) -> Element:
    match expr:
        case ast.Attribute(value=ast.Name(id="VAR"), attr=name):
            return Variable(name)

        case ast.Name(id=ag) if "AG" in activation_groups.__all__:
            ag = int(ag.lstrip("AG"))
            return ActivationGroup.fixed(ag)

        case ast.Name(id=name):
            return Variable(name, is_local=True)

        case ast.Call(func=ast.Name(id="AG"), args=[n]):
            return ActivationGroup(match_expr(n))

        case ast.Call(func=ast.Name(id="Vec"), args=[x, y, z]):
            return Vector(match_expr(x), match_expr(y), match_expr(z))

        case ast.Constant(value=bool() as val):
            return Constant.from_bool(val)

        # int must remain after bool, because it is the superclass of bool
        case ast.Constant(value=int() | float() as val):
            return Constant.from_number(val)

        case ast.Constant(value=str() as val):
            return Constant.from_text(val)

        case ast.BinOp(left=left, op=op, right=right):
            return match_binary_op(left, op, right)

        case ast.Compare(left=left, ops=ops, comparators=right):
            return match_comparison(left, ops, right)

        case ast.BoolOp(op=op, values=values):
            return match_bool_ops(op, values)

        case ast.UnaryOp(op=ast.Not(), operand=operand):
            return Not(match_expr(operand))

        case _:
            raise SyntaxError(
                f"Unexpected expression syntax:\n{ast.unparse(expr)}\n{ast.dump(expr)}"
            )


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
            raise SyntaxError(
                f"Unsupported operation '{ast.unparse(op)}' in\n{ast.unparse((node := ast.BinOp(left, op, right)))}\n{ast.dump(node)}"
            )


def match_comparison(left: ast.expr, ops: list[ast.cmpop], comparators: list[ast.expr]):
    def get_func(op):
        match op:
            case ast.Lt():
                return Comparison.lt
            case ast.LtE():
                return Comparison.lte
            case ast.Gt():
                return Comparison.gt
            case ast.GtE():
                return Comparison.gte
            case ast.Eq():
                return Comparison.eq
            case ast.NotEq():
                return lambda left, right: Not(Comparison.eq(left, right))
            case _:
                raise SyntaxError(
                    f"Unsupported operation '{ast.unparse(op)}' in\n{ast.unparse(node := ast.Compare(left, ops, comparators))}\n{ast.dump(node)}"
                )

    comparisons = [
        get_func(ops[i])(
            match_expr(left if i == 0 else comparators[i - 1]),
            match_expr(comparators[i]),
        )
        for i in range(len(ops))
    ]

    result = comparisons[0]
    for comp in comparisons[1:]:
        result = BoolOp.and_(result, comp)

    return result


def match_bool_ops(op: ast.boolop, values: list[ast.expr]):
    def get_func():
        match op:
            case ast.Or():
                return BoolOp.or_
            case ast.And():
                return BoolOp.and_
            case _:
                raise SyntaxError(
                    f"Unsupported operation '{ast.unparse(op)}' in\n{ast.unparse(node := ast.BoolOp(op, values))}\n{ast.dump(node)}"
                )

    fn = get_func()

    result = fn(match_expr(values[0]), match_expr(values[1]))
    for expr in values[2:]:
        result = fn(result, match_expr(expr))

    return result
