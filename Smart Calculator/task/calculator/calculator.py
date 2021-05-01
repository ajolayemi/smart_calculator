#!/usr/bin/env python

if __name__ == '__main__':
    while True:
        expr = input()
        if expr == '/exit':
            print('Bye!')
            break
        elif expr == '/help':
            print('A simple calculator that only adds values as at now')

        elif expr == '':
            continue

        elif len(expr.split()) == 1:
            print(expr)

        else:
            split_expr = list(map(lambda x: int(x), expr.split()))
            print(sum(split_expr))
