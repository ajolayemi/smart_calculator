#!/usr/bin/env python
import re
from collections import deque

DESCRIPTION = 'A smart calculator capable of handling the following arithmetic operations:\n' \
              '1. Addition and subtraction of two or more numbers\n' \
              '2. Variable declaration and usage in expressions later on\n' \
              'User is prompted to enter the expression they want to ' \
              'evaluate and the evaluation result is printed out.'

# A dict of signs arranged from the lowest in rank to the highest
SIGNS_PRIORITY = {'-': 1,
                  '+': 1,
                  '/': 3,
                  '*': 4,
                  '^': 5,
                  }
invalid_expressions = re.compile(r'^[+-]+$|[+-]$|^[\w\d ]+ [\w\d]+$')
variable_pattern = re.compile(r'^[a-zA-Z]+$')
variable_value_ptn = re.compile(r'^[a-zA-Z]+$|^[\d]+$')
variable_request = re.compile(r'^[a-zA-Z]+$')
variable_expression_ptn = re.compile(r'^[\w +-]+[ +-]+[\w]$')
expression_matcher_ptn = re.compile(r'-[\w]+|[\w]+|[-+*/^ =()]')
commands = ['/help', '/exit']


class Calculator:
    var_value_dict = {}

    def __init__(self, expression: str):
        self.expression = expression
        self.is_var_declaration = '=' in self.expression
        self.is_var_request = re.search(variable_request, self.expression)
        self.is_var_expression = re.search(variable_expression_ptn, self.expression)
        self.postfix_expr = ''
        self.infix_to_postfix()

    def module_caller(self):
        """ Decides which module to call for calculation. """
        if self.is_var_declaration:
            self.var_declaration_handler()

        elif self.is_var_request:
            self.var_request_handler()

        else:
            self.expression_eval()

    def var_request_handler(self):
        """ Responds to when user is requesting to view the value of a
        variable. """
        if self.expression not in Calculator.var_value_dict:
            print('Unknown variable')
        else:
            print(Calculator.var_value_dict.get(self.expression))

    def var_declaration_handler(self):
        """ Responds to when user is trying to declare new variables. """
        variable_name = self.expression[:self.expression.find('=')].strip()
        variable_value = self.expression[self.expression.find('=') + 1:].strip()
        if not self.check_variable_name(variable_name):
            print('Invalid identifier')
        elif not self.check_variable_val_name(variable_value) or \
                self.expression.count('=') > 1:
            print('Invalid assignment')
        elif variable_value.isalpha() and variable_value not in Calculator.var_value_dict:
            print('Unknown variable')
        else:
            if variable_value.isalpha():
                Calculator.var_value_dict[variable_name] = Calculator.var_value_dict.get(variable_value)
            else:
                Calculator.var_value_dict[variable_name] = variable_value

    @staticmethod
    def check_variable_val_name(val_name: str) -> True:
        """ Checks to see that the value of a variable is valid.
        :returns True if val_name is valid
        :returns False otherwise. """
        return re.search(variable_value_ptn, val_name) is not None

    @staticmethod
    def check_variable_name(var_name: str):
        """ Checks to see that variable name is valid.
        :returns True if var_name is valid.
        :returns False otherwise"""
        return re.search(variable_pattern, var_name) is not None

    def expression_eval(self):
        """ Handles expressions that contains variable."""
        value = self.expr_parser()
        try:
            output = 0
            signs = []
            while True:
                current_value = next(value)
                if current_value.isalpha():
                    if not self.check_variable_name(current_value) or \
                            current_value not in Calculator.var_value_dict:
                        print(f'Variable -- {current_value} is unknown.')
                        break
                    else:
                        final_sign = self.sign_calculator(signs)
                        signs.clear()
                        variable_value = int(Calculator.var_value_dict.get(current_value))
                        output = self.calculation_helper(current_value=output,
                                                         sign=final_sign,
                                                         value_to_add_or_sub=variable_value)
                elif current_value in SIGNS_PRIORITY.keys():
                    signs.append(current_value)
                else:
                    final_sign = self.sign_calculator(signs)
                    signs.clear()
                    output = self.calculation_helper(current_value=output,
                                                     sign=final_sign,
                                                     value_to_add_or_sub=current_value)
        except StopIteration:
            print(output)

    @staticmethod
    def calculation_helper(current_value, sign, value_to_add_or_sub):
        """ Helps the two module that handles calculation. """
        if sign == '+':
            return current_value + int(value_to_add_or_sub)
        elif sign == '-':
            return current_value - int(value_to_add_or_sub)

    @staticmethod
    def sign_calculator(signs: list):
        result = None
        if not signs:
            return '+'
        for sign in signs:
            if not result:
                result = sign
            elif sign == '-' and result == '-' or sign == '+' and result == '+':
                result = '+'
            else:
                result = '-'
        return result

    def expr_scanner(self):
        """ Scans the provided expression replacing multiple minus signs
        and addition signs present in it. """
        parenthesis = ['(', ')']
        expr = re.findall(expression_matcher_ptn, self.expression)
        signs = []
        result = ''

        for _, sign_checker in enumerate(expr):
            if sign_checker != ' ':
                negative_num = sign_checker.startswith('-') and len(sign_checker) > 1
                positive_num = sign_checker.startswith('+') and len(sign_checker) > 1
                if sign_checker in SIGNS_PRIORITY.keys():
                    signs.append(sign_checker)

                elif sign_checker.isnumeric() or sign_checker.isalpha() or sign_checker in parenthesis\
                        or negative_num or positive_num:
                    if signs:
                        final_sign = self.sign_calculator(signs)
                        result += f'{final_sign} '
                        result += f'{sign_checker} '
                        signs.clear()
                    else:
                        result += f'{sign_checker} '

        self.expression = result

    def infix_to_postfix(self):
        """ Transforms Infix expressions to Postfix expressions. """
        stack = deque()
        self.expr_scanner()
        expression = re.findall(expression_matcher_ptn, self.expression)
        for expr in expression:
            negative_num = expr.startswith('-') and len(expr) > 1
            positive_num = expr.startswith('+') and len(expr) > 1
            if expr != ' ':
                if expr.isnumeric() or expr.isalpha() or negative_num or positive_num:
                    self.postfix_expr += f'{expr} '
                else:
                    if not stack:
                        stack.append(expr)
                    else:
                        stack_top = stack[-1]
                        stack_top_priority = SIGNS_PRIORITY.get(stack_top, 0)
                        expr_priority = SIGNS_PRIORITY.get(expr, 0)
                        if expr == ')':
                            while True and len(stack) > 0:
                                check_stack = stack[-1]
                                if check_stack != '(':
                                    self.postfix_expr += f'{stack.pop()} '
                                else:
                                    stack.pop()
                                    break

                        elif stack_top == '(' or expr == '(':
                            stack.append(expr)

                        elif expr_priority > stack_top_priority:
                            stack.append(expr)

                        elif expr_priority <= stack_top_priority:
                            while True and len(stack) > 0:
                                check_stack_top = stack[-1]
                                if check_stack_top == '(':
                                    break

                                elif SIGNS_PRIORITY.get(check_stack_top) >= expr_priority:
                                    self.postfix_expr += f'{stack.pop()} '
                                else:
                                    break
                            else:
                                stack.append(expr)

        while len(stack) > 0:
            popped_item = stack.pop()
            if popped_item in SIGNS_PRIORITY.keys():
                self.postfix_expr += f'{popped_item} '

    def expr_parser(self):
        for expr in self.postfix_expr.split():
            if expr != ' ':
                yield expr


def main():

    while True:
        user_expr = input()
        if user_expr.startswith('/') and user_expr not in commands:
            print('Unknown command')
        elif re.search(invalid_expressions, user_expr):
            print('Invalid expression')
        elif not user_expr:
            continue
        elif user_expr == '/exit':
            print('Bye!')
            break
        elif user_expr == '/help':
            print(DESCRIPTION)
        else:
            expr_class = Calculator(user_expr)
            print(expr_class.postfix_expr)


if __name__ == '__main__':
    main()
