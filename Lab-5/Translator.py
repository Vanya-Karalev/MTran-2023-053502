from typing import List, Dict, Any
from Lexer import Lexer
from Token import Token
from Tree import ExpressionNode, ConstantNode, UnaryOperationNode, VariableNode, BinaryOperationNode, ArrayDefinition, \
    Array, CinNode, KeyWordNode, CoutNode, WhileNode, ForNode, IfNode, FunctionNode, FunctionCallNode, SwitchNode, \
    CaseNode, ReturnNode, StatementsNode


class Translator:
    def __init__(self, tree):
        self.code = self.create(tree)
        print(self.code)

    def create(self, node, depth=0):
        if isinstance(node, Statement):
            return self.create_statement(node, depth)
        elif isinstance(node, BinaryOperation):
            return self.create_binary_operation(node)
        elif isinstance(node, KeyWord):
            return self.create_key_word(node)
        elif isinstance(node, CIn):
            return self.create_cin(node)
        elif isinstance(node, COut):
            return self.create_cout(node)
        elif isinstance(node, While):
            return self.create_while(node, depth)
        elif isinstance(node, For):
            return self.create_for(node, depth)
        elif isinstance(node, If):
            return self.create_if(node, depth)
        elif isinstance(node, Return):
            return self.create_return(node)
        elif isinstance(node, FunctionCall):
            return self.create_function_call(node)
        elif isinstance(node, Variable):
            return self.create_variable(node)
        elif isinstance(node, UnaryOperation):
            return self.create_unary_operation(node)
        elif isinstance(node, Constant):
            return self.create_constant(node)
        elif isinstance(node, Array):
            return self.create_array(node)

    def create_statement(self, node, depth):
        result = ''
        for entity in node.nodes:
            result += depth * '\t' + f'{self.create(entity, depth)}\n'
        return result[:-1]

    def create_binary_operation(self, node):
        left = self.create(node.left_node)
        right = self.create(node.right_node)
        operation = node.operation.word
        if operation == '&&': operation = 'and'
        elif operation == '||': operation = 'or'
        elif operation == '[': return f'{left}[{right}]'
        elif operation == '.': return f'{left}.{right}'
        return f'{left} {operation} {right}'

    def create_key_word(self, node):
        if node.word.word == 'endl': return '"\\n"'
        elif node.word.word == 'continue': return 'continue'
        elif node.word.word == 'break' and not self._switch: return 'break'
        return ''

    def create_cin(self, node):
        inputs = 'input()'
        for var in node.expression:
            data_type = var.variable.token_type.split()[0].lower()
            inputs += f', {data_type}(input())' if data_type != 'int' and data_type != 'float' else ', input()'
        return f'{self.create(node.expression[0])} = {inputs}'

    def create_cout(self, node):
        expression = f'print({self.create(node.expression[0])}'
        for val in node.expression[1:]:
            expression += f', {self.create(val)}'
        return expression + ', end="")'

    def create_while(self, node, depth):
        result = f'while {self.create(node.condition)}:\n'
        result += self.create(node.body, depth + 1)
        return result

    def create_for(self, node, depth):
        if not node.begin:
            result = f'while(True):\n'
            result += self.create(node.body, depth + 1)
            return result
        variable = node.begin.left_node.variable.word
        begin = node.begin.right_node.constant.word
        operation = node.condition.operation.word
        end = self.create(node.condition.right_node)
        loop_range = f'{begin}, {end}' if operation in ('<', '>') else f'{begin}, {end} + 1'
        step = '-1' if node.step.operation.word == '--' else '1' if node.step.operation.word == '++' else self.create(node.step.right_node) if node.step.operation.word == '+=' else f'-{self.create(node.step.right_node)}'
        return f'for {variable} in range({loop_range}, {step}):\n' + self.create(node.body, depth + 1)

    def create_if(self, node, depth):
        result = f'if {self.create(node.condition)}:\n'
        result += self.create(node.body, depth + 1)
        if node.else_condition:
            statement = self.create(node.else_condition, depth)        if statement.startswith('if'):
            result += f'{depth * "\t"}else {statement[2:]}'
        else:
            result += f'{depth * "\t"}else:\n{statement}'
        return result

    def create_return(self, node):
        return f'return {self.create(node.expression)}'

    def create_function_call(self, node):
        function_name = node.function_name.word
        arguments = ''
        for arg in node.arguments:
            if isinstance(arg, Variable):
                arguments += f'{arg.word}, '
            else:
                arguments += f'{self.create(arg)}, '
        arguments = arguments[:-2]
        return f'{function_name}({arguments})'

    def create_variable(self, node):
        if node.variable.word in ct_var:
            return f'{ct_var[node.variable.word]}({self.create(node.expression)})'
        return node.variable.word

    def create_unary_operation(self, node):
        expression = self.create(node.expression)
        if node.operation.word in un_op:
            return f'{un_op[node.operation.word]}{expression}'
        return f'{expression}{node.operation.word}'

    def create_constant(self, node):
        if node.token_type in ('STRING', 'CHAR'):
            return f'"{node.word}"'
        return node.word

    def create_array(self, node):
        if node.is_empty:
            return empt_arr
        elements = ''
        for element in node.elements:
            if isinstance(element, Array):
                elements += f'{self.create_array(element)}, '
            else:
                elements += f'{self.create(element)}, '
        return f'[{elements[:-2]}]'
