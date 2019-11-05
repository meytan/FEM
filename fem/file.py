import ast

with open('fem\components.py') as f:
    tree = ast.parse(f.read()) 

pass