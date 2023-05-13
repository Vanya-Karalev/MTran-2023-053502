from abc import ABC
from Token import Token


class ExpressionNode(ABC):
    pass


class StatementsNode(ExpressionNode):
    def __init__(self):
        self.nodes = []

    def add_node(self, node: ExpressionNode):
        self.nodes.append(node)


class VariableNode(ExpressionNode):
    def __init__(self, variable):
        self.variable = variable


class VariableTypeNode(ExpressionNode):
    def __init__(self, variable_type: Token):
        self.variable_type = variable_type


class BinaryOperationNode(ExpressionNode):
    def __init__(self, operation: Token, left_node: ExpressionNode, right_node: ExpressionNode):
        self.operation = operation
        self.left_node = left_node
        self.right_node = right_node


class UnaryOperationNode(ExpressionNode):
    def __init__(self, operation: Token, node: ExpressionNode):
        self.operation = operation
        self.node = node


class CinNode(ExpressionNode):
    def __init__(self, expression: list):
        self.expression = expression


class ConstantNode(ExpressionNode):
    def __init__(self, constant):
        self.constant = constant


class CoutNode(ExpressionNode):
    def __init__(self, expression: list):
        self.expression = expression


class ForNode(ExpressionNode):
    def __init__(self, begin: ExpressionNode, condition: ExpressionNode, step: ExpressionNode, body: ExpressionNode):
        self.begin = begin
        self.condition = condition
        self.step = step
        self.body = body


class FunctionCallNode(ExpressionNode):
    def __init__(self, name: Token, parameters: list):
        self.name = name
        self.parameters = parameters


class FunctionNode(ExpressionNode):
    def __init__(self, name: Token, parameters: list, body: ExpressionNode):
        self.name = name
        self.parameters = parameters
        self.body = body


class IfNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: ExpressionNode, else_condition=None):
        self.condition = condition
        self.body = body
        self.else_condition = else_condition


class KeyWordNode(ExpressionNode):
    def __init__(self, word: Token):
        self.word = word


class ReturnNode(ExpressionNode):
    def __init__(self, statement: ExpressionNode):
        self.statement = statement


class SwitchNode(ExpressionNode):
    def __init__(self, variable: Token, body: ExpressionNode):
        self.variable = variable
        self.body = body


class WhileNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: ExpressionNode):
        self.condition = condition
        self.body = body


class Array(ExpressionNode):
    def __init__(self, elements: list):
        self.elements = elements


class ArrayDefinition(ExpressionNode):
    def __init__(self, variable: ExpressionNode, sizes: list):
        self.variable = variable
        self.sizes = sizes


class CaseNode(ExpressionNode):
    def __init__(self, variable: Token):
        self.variable = variable
