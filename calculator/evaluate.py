with open('expression.txt', 'r') as f:
    expression = f.read()

result = eval(expression)
print(result)