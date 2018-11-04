# Code must have a spacebar between all of tokens.

from stack import Stack
from scanner import Scanner

file = open('./terminal.txt', 'r')
terminal = set([str(line.strip()) for line in file])
nonTerminal = set()
file.close()

startSymbol = 'pgm'
lamda = 'EMPTY'
grammar = dict()
haveEmpty = set()

file = open('./grammar.txt', 'r')
ig = 1
for line in file:
    tmp = line.strip().split()
    key = tmp[0]
    nonTerminal.add(key)
    tmp = tmp[2:]
    grammar[ig] = {key: []}
    a = []
    for i in range(len(tmp)):
        if tmp[i] == '|':
            grammar[ig][key] = a
            a = []
            ig += 1
            grammar[ig] = {key: []}
            continue
        if i == len(tmp)-1:
            a.append(tmp[i])
            grammar[ig][key] = a
            ig += 1
            a = []
        if tmp[i] == "EMPTY":
            haveEmpty.add(key)
        a.append(tmp[i])
file.close()


scan = Scanner("./input.txt")
stream = scan.getStream()

parsing_table = {"pgm": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                 "line": [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "stmt": [0, 4, 0, 5, 6, 7, 8, 0, 0, 0, 0, 0],
                 "asgmnt": [0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "exp1": [0, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "exp2": [13, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 13],
                 "term": [0, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "if": [0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0],
                 "cond1": [0, 17, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "cond2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 19, 0],
                 "print": [0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0],
                 "goto": [0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0],
                 "stop": [0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0]}

output = []
valid = True

s = Stack()
s.push("EOF")
s.push(startSymbol)

index = 0


def updateOutput(type, val):
    global output, valid
    if type == 'line_num':
        if val < 1 or val > 1000:
            valid = False
            print("line_num out of range.")
            return
        if len(output) > 0 and output[-1] == 14:
            output.append(val)
        elif len(output) > 7 and output[-8] == 13:
            output.append(14)
            output.append(val)
        else:
            output.append(10)
            output.append(val)
    elif type == 'id':
        output.append(11)
        output.append(val+1)
    elif type == 'const':
        if val < 0 or val > 100:
            valid = False
            print("const out of range.")
            return
        output.append(12)
        output.append(val)
    elif type == 'IF':
        output.append(13)
        output.append(0)
    elif type == 'GOTO':
        output.append(14)
    elif type == 'PRINT':
        output.append(15)
        output.append(0)
    elif type == 'STOP':
        output.append(16)
        output.append(0)
    elif type == '+':
        output.append(17)
        output.append(1)
    elif type == '-':
        output.append(17)
        output.append(2)
    elif type == '<':
        output.append(17)
        output.append(3)
    elif type == '=':
        output.append(17)
        output.append(4)


def match(top, type):
    return top == type or (top == "line_num" and type == "number") or (top == "const" and type == "number")


def T(A, a):
    global parsing_table
    row = parsing_table[A]
    select = 0
    if a == "number" and row[0] != 0:
        select = row[0]
    elif a == "id":
        select = row[1]
    elif a == "number" and row[2] != 0:
        select = row[2]
    elif a == "IF":
        select = row[3]
    elif a == "PRINT":
        select = row[4]
    elif a == "GOTO":
        select = row[5]
    elif a == "STOP":
        select = row[6]
    elif a == "+":
        select = row[7]
    elif a == "-":
        select = row[8]
    elif a == "<":
        select = row[9]
    elif a == "=":
        select = row[10]
    elif a == "EOF":
        select = row[11]
    if select == 0:
        return []
    else:
        return grammar[select][A]


while index <= len(stream)-1 and not s.isEmpty():
    top = s.top()
    token = stream[index]
    type, value = token
    if top in terminal and match(top, type):
        updateOutput(top, value)
        if not valid:
            break
        s.pop()
        index += 1
    elif top in nonTerminal:
        l = T(top, type)
        if len(l) == 0:
            valid = False
            break
        s.pop()
        for i in range(len(l)-1, -1, -1):
            if l[i] == lamda:
                continue
            s.push(l[i])

if not s.isEmpty or index != len(stream):
    valid = False
if valid:
    file = open("./output.txt", "w")
    for o in output:
        file.write(str(o))
        file.write(" ")
    file.close()
    print("Finished, check output.txt file.")
else:
    print("Error, please fix your code.")
