import re
from Lexer import Lexer
from Token import Token
from Tree import ExpressionNode, ConstantNode, UnaryOperationNode, VariableNode, BinaryOperationNode, ArrayDefinition, \
    Array, CinNode, KeyWordNode, CoutNode, WhileNode, ForNode, IfNode, FunctionNode, FunctionCallNode, SwitchNode, \
    CaseNode, ReturnNode, StatementsNode


class Semantic:
    def __init__(self, parser: SyntaxParser):
        self.Variables: Dict[str, str] = parser.Variables
        self.Funcs: Dict[str, str] = parser.Funcs
        self.cycleLevel = 0
        self.conditionalLevel = 0

    def CheckType(self, type1: str, type2: str) -> bool:
        if type1 != type2:
            if type1 == "float" and type2 == "int":
                return True
            if type1 == "int" and type2 == "float":
                return True
            if type1 == "int" and type2 == "char":
                return True
            if type1 == "char" and type2 == "int":
                return True
            return False
        return True

    def Parse(self, rootNode: Union[INode, None]) -> Union[str, None]:
        if rootNode is None:
            return None

        if isinstance(rootNode, BlockNode):
            for elem in rootNode.Nodes:
                self.Parse(elem)

        if isinstance(rootNode, FunctionNode):
            for elem in functionNode.Parameters:
                print(elem.Value)
            self.Parse(functionNode.Body)

        if isinstance(rootNode, WhileNode):
            self.Parse(whileNode.Condition)
            self.cycleLevel += 1
            self.Parse(whileNode.Body)
            self.cycleLevel -= 1

        if isinstance(rootNode, ConditionalNode):
            self.Parse(ifNode.Condition)
            self.conditionalLevel += 1
            self.Parse(ifNode.Body)
            self.Parse(ifNode.ElseBody)
            self.conditionalLevel -= 1

        if isinstance(rootNode, CycleKeywordsNode):
            if self.cycleLevel == 0 or self.conditionalLevel == 0:
                raise Exception(f"Incorrect usage of {cycleKeywordsNode.Keyword.Value}")

        if isinstance(rootNode, CoutNode):
            for elem in coutNode.Parameters:
                self.Parse(elem)

        if isinstance(rootNode, CinNode):
            for elem in cinNode.Parameters:
                self.Parse(elem)

        if isinstance(rootNode, ForNode):
            self.Parse(forNode.Init)
            self.Parse(forNode.Condition)
            self.Parse(forNode.Iterator)
            self.cycleLevel += 1
            self.Parse(forNode.Body)
            self.cycleLevel -= 1

        if isinstance(rootNode, BinaryOperationNode):
            type1 = type2 = None
            variableString = ""
            if rootNode.Operator.Type == TokenType.NEW:
                if isinstance(rootNode.RightNode, VariableNode):
                    if self.Variables[rootNode.RightNode.Variable.Value] != "int":
                        raise Exception("Size of array must be int")
                elif isinstance(rootNode.RightNode, ConstNode):
                    if rootNode.RightNode.Constant.Value.Type != "int":
                        raise Exception("Size of array must be int")
                else:
                    raise Exception("Size of array must be int")
                if isinstance(rootNode.LeftNode, VariableTypeNode):
                    return f"{rootNode.LeftNode.VariableType.Value} array"

            if isinstance(rootNode.LeftNode, VariableNode):
                regex = re.compile(r"^(\w*\.)?\w+\(.*\)")
                match = regex.match(rootNode.LeftNode.Variable.Value)
                match2 = re.sub(r"\(.*)", "", rootNode.LeftNode.Variable.Value)
                if match and match2 in self.Funcs.keys():
                    # If left node is a function call, we need to get its return type to check against the right node
                    type1 = self.Funcs[match2]
                else:
                    variableString = rootNode.LeftNode.Variable.Value
                    type1 = self.Variables[variableString]

            if isinstance(rootNode.RightNode, VariableNode):
                regex = re.compile(r"^(\w*\.)?\w+\(.*\)")
                match = regex.match(rootNode.RightNode.Variable.Value)
                match2 = re.sub(r"\(.*\)", "", rootNode.RightNode.Variable.Value)

                if match and match2 in self.Funcs.keys():
                    # If right node is a function call, we need to get its return type to check against the left node
                    type2 = self.Funcs[match2]
                else:
                    variableString = rootNode.RightNode.Variable.Value
                    type2 = self.Variables[variableString]

            if isinstance(rootNode.LeftNode, ConstNode):
                type1 = rootNode.LeftNode.Constant.Value.Type

            if isinstance(rootNode.RightNode, ConstNode):
                type2 = rootNode.RightNode.Constant.Value.Type

            if not self.CheckType(type1, type2):
                raise Exception(
                    f"Type mismatch in expression: {variableString} {rootNode.Operator.Value} {rootNode.RightNode.Variable.Value}")

            if isinstance(rootNode, VariableNode):
                if rootNode.Variable.Value not in self.Variables.keys():
                    raise Exception(f"Undefined variable {rootNode.Variable.Value}")

            return None
