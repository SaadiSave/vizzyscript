import ast
from dataclasses import dataclass
from typing import Self
from vizzy_api import triggers
from . import matchers as m
from . import xml_gen as gen

__all__ = ["Program", "Parser"]

normal_triggers = filter(lambda s: s.islower(), triggers.__all__)


@dataclass
class Function:
    source: ast.FunctionDef
    name: str
    params: list[str]

    @classmethod
    def from_function_def(cls, source: ast.FunctionDef) -> Self:
        return cls(source, source.name, [a.arg for a in source.args.args])

    def __str__(self) -> str:
        return f"locals: {self.params}\nunparsed:\n{ast.unparse(self.source)}"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Function):
            return self.name == value.name

        return False


@dataclass
class Target:
    threads: list[Function]
    msg: str | None = None

    def add_thread(self, f: Function):
        self.threads.append(f)


class Program:
    def __init__(self, tree: ast.AST) -> None:
        assert isinstance(tree, ast.Module)
        self.tree: ast.Module = tree
        self.functions: set[Function] = set()
        self.threads: dict[str, Target] = {
            trigger: Target([]) for trigger in normal_triggers
        }
        self.variables: list[str] = []
        self.lists: list[str] = []

    def find_channels(self):
        for stmt in self.tree.body:
            match stmt:
                case ast.Assign(
                    targets=[ast.Name(id=channel)],
                    value=ast.Call(
                        func=ast.Name(id=chan_type)
                        | ast.Subscript(value=ast.Name(id=chan_type)),
                        args=[ast.Constant(value=msg)],
                    ),
                ) if (
                    "Channel" in chan_type
                ):
                    self.threads[channel] = Target([], msg)

    def find_functions(self):
        for stmt in self.tree.body:
            if isinstance(stmt, ast.FunctionDef):
                self.functions.add(Function.from_function_def(stmt))

    def link_threads(self):
        for stmt in self.tree.body:
            match stmt:
                case ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id=trigger)
                        | ast.Attribute(value=ast.Name(id=trigger), attr="receive"),
                        args=[ast.Name(id=target)],
                    )
                ) if (
                    trigger in self.threads
                ):
                    links = {func for func in self.functions if func.name == target}
                    for func in links:
                        self.threads[trigger].add_thread(func)
                        self.functions.remove(func)

    def find_vars(self):
        for stmt in self.tree.body:
            if isinstance(stmt, ast.ClassDef) and stmt.name == "VAR":
                for var in stmt.body:
                    match var:
                        case ast.AnnAssign(
                            target=ast.Name(id=name), annotation=ast.Name(id=datatype)
                        ):

                            if "list" in datatype:
                                self.lists.append(name)
                            else:
                                self.variables.append(name)


class Parser:
    def __init__(self, name: str, src: str) -> None:
        self.root = gen.Program(name)

        self.program = Program(ast.parse(src))

        self.program.find_channels()
        self.program.find_functions()
        self.program.find_vars()

        self.program.link_threads()

        self.root.append(gen.Variables(self.program.variables))
        self.root.append(gen.Expressions())

    def generate(self):
        for trigger, target in self.program.threads.items():  #
            self.__generate_thread(trigger, target)

    def __generate_thread(self, trigger: str, t: Target):
        # TODO: implement other triggers

        threads = [
            [m.match_statement(stmt) for stmt in body]
            for body in [i.source.body for i in t.threads]
        ]

        for thread in threads:
            if t.msg is not None:
                self.root.append(gen.ReceiveMessage(t.msg, thread))
