from Lexer import Lexer
from Token import Token
from Tree import ExpressionNode, ConstantNode, UnaryOperationNode, VariableNode, BinaryOperationNode, ArrayDefinition, \
    Array, CinNode, KeyWordNode, CoutNode, WhileNode, ForNode, IfNode, FunctionNode, FunctionCallNode, SwitchNode, \
    CaseNode, ReturnNode, StatementsNode


class Parser:
    def __init__(self, lexer: Lexer):
        self.tokens = lexer.tokens
        self.position = 0

        # Store token lists from lexer for reference
        self.key_words = lexer.key_word_tokens
        self.constants = lexer.constants_tokens.keys()
        self.variable_types = lexer.var_types_tokens
        self.variables = lexer.var_tokens.keys()
        self.functions = lexer.func_tokens.keys()

    def match(self, expected: []) -> Token:
        # Check if current token matches an expected token
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if current_token.word in expected:
                self.position += 1
                return current_token
        return None

    def get_prev_token_word(self) -> str:
        # Get the word of the previous token
        return self.tokens[self.position - 1].word

    def require(self, expected: []) -> Token:
        # Check if current token matches an expected token, raise exception if not
        token = self.match(expected)
        if token is None:
            raise Exception(f'Expected {expected} after {self.get_prev_token_word()} in position {self.position - 1}')
        return token

    def parse_code_block(self) -> ExpressionNode:
        # Parse a block of code, i.e., statements within curly braces
        root = StatementsNode()
        while self.position < len(self.tokens):
            if self.match(['}']):
                self.position -= 1
                return root
            # Parse an expression and add it to the root node
            code_string_node = self.parse_expression()
            if code_string_node:
                if isinstance(code_string_node, list):
                    for node in code_string_node:
                        root.add_node(node)
                else:
                    root.add_node(code_string_node)
        return root

    def parse_expression(self) -> ExpressionNode:
        # Parse an expression
        key_word_token = self.match(self.key_words)
        if key_word_token:
            # Handle various keywords
            if key_word_token.word == 'case':
                return self.parse_case()
            elif key_word_token.word == 'default':
                return self.parse_key_word(key_word_token)
            elif key_word_token.word == 'cin':
                return self.parse_cin()
            elif key_word_token.word == 'cout':
                return self.parse_cout()
            elif key_word_token.word == 'for':
                return self.parse_for()
            elif key_word_token.word == 'if':
                return self.parse_if_else_condition()
            elif key_word_token.word == 'switch':
                return self.parse_switch()
            elif key_word_token.word in ['continue', 'break']:
                return self.parse_key_word(key_word_token)
            elif key_word_token.word == 'while':
                return self.parse_while()
            elif key_word_token.word == 'return':
                return self.parse_return()
        variable_token = self.match(self.variables)
        if variable_token:
            # Handle a variable or constant
            self.position -= 1
            var_node = self.parse_variable_or_constant()
            operation = self.match(['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '!', '?', '==', '!=        ])
            if operation:
            # Handle a binary operation
                right_node = self.parse_expression()
            if not right_node:
                raise Exception(f'Expected expression after {operation.word} in position {self.position - 1}')
            return BinaryOperationNode(var_node, operation, right_node)
        return var_node

    constant_token = self.match(self.constants)
    if constant_token:
        # Handle a constant
        return ConstantNode(constant_token)
    if self.match(['(']):
        # Handle a function call
        function_token = self.require(self.functions)
        args = []
        while not self.match([')']):
            arg = self.parse_expression()
            if not arg:
                raise Exception(f'Expected expression in position {self.position - 1}')
            args.append(arg)
            self.match([','])
        return FunctionCallNode(function_token, args)
    if self.match(['[']):
        # Handle an array definition
        size = self.parse_expression()
        if not size:
            raise Exception(f'Expected array size in position {self.position - 1}')
        self.require([']'])
        return ArrayDefinition(variable_token, size)
    return None


def parse_variable_or_constant(self) -> Union[VariableNode, ConstantNode]:
    # Parse a variable or constant
    variable_token = self.match(self.variables)
    if variable_token:
        # Handle a variable
        if self.match(['[']):
            # Handle an array index
            index = self.parse_expression()
            if not index:
                raise Exception(f'Expected array index in position {self.position - 1}')
            self.require([']'])
            return Array(variable_token, index)
        return VariableNode(variable_token)
    constant_token = self.match(self.constants)
    if constant_token:
        # Handle a constant
        return ConstantNode(constant_token)
    return None


def parse_unary_operation(self) -> UnaryOperationNode:
    # Parse a unary operation
    operation = self.match(['-', '+', '!'])
    if not operation:
        return None
    node = self.parse_expression()
    if not node:
        raise Exception(f'Expected expression after {operation.word} in position {self.position - 1}')
    return UnaryOperationNode(operation, node)


def parse_if_else_condition(self) -> IfNode:
    # Parse an if statement
    self.require(['('])
    condition = self.parse_expression()
    if not condition:
        raise Exception(f'Expected expression in position {self.position - 1}')
    self.require([')'])
    true_block = self.parse_code_block()
    false_block = None
    if self.match(['else']):
        false_block = self.parse_code_block()
    return IfNode(condition, true_block, false_block)


def parse_for(self) -> ForNode:
    # Parse a for loop
    self.require(['('])
    init = self.parse_expression()
    if not init:
        init = StatementsNode()
    self.require([';'])
    condition = self.parse_expression()
    if not condition:
        raise Exception(f'Expected expression in position {self.position - 1}')
    self.require([';'])
    iteration = self.parse_expression()
    if not iteration:
        iteration = StatementsNode()
    self.require([')'])
    code_block = self.parse_code_block()
    return ForNode(init, condition, iteration, code_block)


def parse_while(self) -> WhileNode:
    # Parse a while loop
    self.require(['('])
    condition = self.parse_expression()
    if not condition:
        raise Exception(f'Expected expression in position {self.position - 1}')
    self.require([')'])
    code_block = self.parse_code_block()
    return WhileNode(condition, code_block)


def parse_code_block(self) -> StatementsNode:
    # Parse a code block
    self.require(['{'])
    statements = StatementsNode()
    while not self.match(['}']):
        statement = self.parse_statement()
        if not statement:
            raise Exception(f'Expected statement in position {self.position - 1}')
        statements.add(statement)
    return statements


def parse_function_definition(self) -> FunctionNode:
    # Parse a function definition
    self.require(['function'])
    name = self.require(self.variables)
    self.require(['('])
    args = []
    while not self.match([')']):
        arg_name = self.require(self.variables)
        args.append(arg_name)
        self.match([','])
    code_block = self.parse_code_block()
    return FunctionNode(name, args, code_block)


def parse_statement(self) -> ExpressionNode:
    # Parse a statement
    node = self.parse_if_else_condition()
    if node:
        return node
    node = self.parse_for()
    if node:
        return node
    node = self.parse_while()
    if node:
        return node
    node = self.parse_function_definition()
    if node:
        return node
    node = self.parse_expression()
    if node:
        self.match([';'])
        return node
    return None


def parse(self) -> StatementsNode:
    # Parse the input
    statements = StatementsNode()
    while self.tokens:
        statement = self.parse_statement()
        if not statement:
            raise Exception(f'Expected statement in position {self.position - 1}')
        statements.add(statement)
    return statements


def require(self, kinds: List[str]) -> Token:
    token = self.match(kinds)
    if not token:
        raise Exception(f'Expected token of kind {kinds} in position {self.position - 1}')
    return token


def parse_primary(self) -> Union[VariableNode, ConstantNode, Array, FunctionCallNode, UnaryOperationNode]:
    token = self.match(['('])
    if token:
        node = self.parse_expression()
        self.require([')'])
        return node
    token = self.match(self.variables)
    if token:
        if self.match(['(']):
            args = []
            while not self.match([')']):
                arg = self.parse_expression()
                args.append(arg)
                self.match([','])
            return FunctionCallNode(token, args)
        elif self.match(['[']):
            index = self.parse_expression()
            self.require([']'])
            return Array(token, index)
        else:
            return VariableNode(token)
    token = self.match(self.constants)
    if token:
        return ConstantNode(token)
    raise Exception(f'Expected primary expression in position {self.position - 1}')


def parse_array_definition(self) -> ArrayDefinition:
    variable_token = self.require(self.variables)
    self.require(['['])
    size = self.parse_expression()
    self.require([']'])
    return ArrayDefinition(variable_token, size)


def parse_unary(self) -> Union[UnaryOperationNode, ExpressionNode]:
    token = self.match(['-', '!'])
    if token:
        node = self.parse_primary()
        return UnaryOperationNode(token, node)
    return self.parse_array_definition()


def parse_multiplicative(self) -> ExpressionNode:
    node = self.parse_unary()
    while True:
        token = self.match(['*', '/', '%'])
        if not token:
            return node
        right = self.parse_unary()
        node = BinaryOperationNode(node, token, right)


def parse_additive(self) -> ExpressionNode:
    node = self.parse_multiplicative()
    while True:
        token = self.match(['+', '-'])
        if not token:
            return node
        right = self.parse_multiplicative()
        node = BinaryOperationNode(node, token, right)


def parse_relational(self) -> ExpressionNode:
    node = self.parse_additive()
    while True:
        token = self.match(['<', '>', '<=', '>='])
        if not token:
            return node
        right = self.parse_additive()
        node = BinaryOperationNode(node, token, right)


def parse_equality(self) -> ExpressionNode:
    node = self.parse_relational()
    while True:
        token = self.match(['==', '!='])
        if not token:
            return node
        right = self.parse_relational()
        node = BinaryOperationNode(node, token, right)


def parse_expression(self) -> ExpressionNode:
    return self.parse_equality()


def parse_if_else_condition(self) -> Union[IfNode, None]:
    token = self.match(['if'])
    if not token:
        return None
    self.require(['('])
    condition = self.parse_expression()
    self.require([')'])
    true_block = self.parse_code_block()
    false_block = None
    if self.match(['else']):
        false_block = self.parse_code_block()
    return IfNode(condition, true_block, false_block)


def parse_for(self) -> Union[ForNode, None]:
    token = self.match(['for'])

    if not token:
        return None
    self.require(['('])
    init = self.parse_statement()
    self.require([';'])
    condition = self.parse_expression()
    self.require([';'])
    increment = self.parse_expression()
    self.require([')'])
    block = self.parse_code_block()
    return ForNode(init, condition, increment, block)


def parse_while(self) -> Union[WhileNode, None]:
    token = self.match(['while'])
    if not token:
        return None
    self.require(['('])
    condition = self.parse_expression()
    self.require([')'])
    block = self.parse_code_block()
    return WhileNode(condition, block)


def parse_statement(self) -> Union[ExpressionNode, None]:
    node = self.parse_expression()
    if node is not None:
        return node
    node = self.parse_if_else_condition()
    if node is not None:
        return node
    node = self.parse_for()
    if node is not None:
        return node
    node = self.parse_while()
    if node is not None:
        return node
    return None


def parse_code_block(self) -> CodeBlockNode:
    nodes = []
    self.require(['{'])
    while not self.match(['}']):
        node = self.parse_statement()
    if node is not None:
        nodes.append(node)
    return CodeBlockNode(nodes)


def parse(self) -> ExpressionNode:
    nodes = []
    while self.position < len(self.tokens):
        node = self.parse_statement()
    if node is not None:
        nodes.append(node)
    return ProgramNode(nodes)


def get_tree(node):
    tree = []
    if node is None:
        return
    if isinstance(node, Token):
        return node.word
    elif isinstance(node, list):
        for n in node:
            tree.append([get_tree(n)])
    elif isinstance(node, StatementsNode):
        for n in node.nodes:
            tree.append(get_tree(n))
    elif isinstance(node, UnaryOperationNode):
        tree.append(get_tree(node.node))
        tree.append(node.operation.word)
    elif isinstance(node, BinaryOperationNode):
        tree.append(get_tree(node.left_node))
        tree.append(node.operation.word)
        tree.append(get_tree(node.right_node))
    elif isinstance(node, VariableNode):
        tree.append(node.variable.word)
    elif isinstance(node, ConstantNode):
        tree.append(node.constant.word)
    elif isinstance(node, KeyWordNode):
        tree.append(node.word.word)
    elif isinstance(node, CinNode):
        tree.append('cin')
        result = []
        tree.append(get_tree(node.expression))
        tree.append(result)
    elif isinstance(node, CoutNode):
        tree.append('cout')
        result = []
        tree.append(get_tree(node.expression))
        tree.append(result)
    elif isinstance(node, WhileNode):
        tree.append('while')
        tree.append(get_tree(node.condition))
        tree.append(get_tree(node.body))
    elif isinstance(node, ForNode):
        tree.append('for')
        tree.append(get_tree(node.begin))
        tree.append(get_tree(node.condition))
        tree.append(get_tree(node.step))
        tree.append(get_tree(node.body))
    elif isinstance(node, IfNode):
        tree.append('if')
        tree.append(get_tree(node.condition))
        tree.append(get_tree(node.body))
        if node.else_condition:
            tree.append('else')
            tree.append(get_tree(node.else_condition))
    elif isinstance(node, FunctionNode):
        tree.append('function')
        tree.append(node.name.word)
        tree.append(get_tree(node.parameters))
        tree.append([get_tree(node.body)])
    elif isinstance(node, FunctionCallNode):
        tree.append(node.name.word)
        tree.append(get_tree(node.parameters))
    elif isinstance(node, SwitchNode):
        tree.append('switch')
        tree.append(node.variable.word)
        tree.append(get_tree(node.body))
    elif isinstance(node, CaseNode):
        tree.append('case')
        tree.append(node.variable.word)
    elif isinstance(node, ArrayDefinition):
        tree.append(node.variable.variable.word)
        tree.append('size:')
        tree.append(get_tree(node.sizes))
    elif isinstance(node, Array):
        tree.append(get_tree(node.elements))
    elif isinstance(node, ReturnNode):
        tree.append('return')
        tree.append([get_tree(node.statement)])

    if len(tree) == 0 or len(tree) > 1:
        return tree

    return tree[0]
