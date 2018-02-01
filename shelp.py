import sys, os, time
args = sys.argv
filename = args[1]

class Text(object):
    def __init__(self, lemma):
        self.text = lemma[1:-1]
    def __str__(self):
        return self.text
    def inCode(self):
        return '"' + self.text + '"'

class Number(object):
    def __init__(self, lemma):
        self.number = float(lemma)
    def __str__(self):
        return str(self.number)
    def inCode(self):
        return self.number
    def sum(terms):
        return sum(map((lambda x: x.number), terms))
    def diff(terms):
        terms = list(terms)
        return terms[0].number - Number.sum(terms[1:])
    def mult(terms):
        terms = list(terms)
        total = 1
        for i in terms:
            total *= i.number
        return total
    def div(terms):
        terms = list(terms)
        return terms[0].number / Number.mult(terms[1:])
def get(lemma):
    if lemma[0] == '"' and lemma[-1] == '"':
        return Text(lemma)
    else:
        return Number(lemma)
def getItems(exp):
    readingObject = False
    cue = ''
    obj = ''
    objects = []
    for char in exp:
        if readingObject:
            if not char == cue:
                pass
            else:
                readingObject = False
                obj += char if not char == ' ' else ''
                objects.append(obj)
                cue = ''
                obj = ''

        else:
            if char == '"':
                readingObject = True
                cue = '"'
                obj = ''
            elif not char == ' ':
                readingObject = True
                cue = ' '
                obj = ''
        obj += char
    if not (obj == '' or obj == '"'):
        objects.append(obj)
    return objects

def operate(operator, arguments):
    #print('operating: ' + operator + ' ' + ' '.join(a for a in arguments))
    result = None
    if operator == 'PRINT':
        result = ''
        for arg in arguments:
            result += '\n' + str(get(arg))
        result = result[1:]
        print(result)
        return True
    elif operator == 'YIELD':
        #print('yielded ' + arguments[0])
        return arguments[0]
    elif operator == '+':
        return Number.sum(map((lambda x: get(x)), arguments))
    elif operator == '-':
        return Number.diff(map((lambda x: get(x)), arguments))
    elif operator == '*':
        return Number.mult(map((lambda x: get(x)), arguments))
    elif operator == '/':
        return Number.div(map((lambda x: get(x)), arguments))
    else:
        return None

def evaluate(exp, top=None):
    if exp == '' or exp == ' ':
        return None
    evaluated = False
    top = True if top == None else top
    #print(exp + ' ' + str(top))
    while not evaluated:
        #print('loop started!')
        #time.sleep(0.1)
        #print('EXP: ' + exp)
        readingParen = False
        subExp = ''
        bottom = True
        #print('Evaluating ' + exp)
        parenDepth = 0
        cut1 = 0
        cut2 = 0
        count = 0
        foundCut = False
        for char in exp:
            if not foundCut:
                if not readingParen:
                    if char == '(':
                        readingParen = True
                        cut1 = count
                        parenDepth = 1
                        #print('found paren')
                        bottom = False
                    else:
                        pass
                else:
                    if char == '(':
                        parenDepth += 1
                    if char == ')':
                        parenDepth -= 1
                    if parenDepth == 0:
                        readingParen = False
                        simplified = str(evaluate(subExp, False))
                        #print(simplified)
                        cut2 = count + 1
                        exp = exp[:cut1] + simplified + exp[cut2:]
                        #print('new exp: ' + exp)
                        foundCut = True
                    else:
                        subExp += char
            #print('hopefully unchanged exp: ' + exp)
            count += 1
        #print('hopefully still unchanged exp: ' + exp)
        if bottom:
            #print('reached bottom: ' + exp)
            words = getItems(exp)
            #print(exp + ' ' + str(words))
            operator = words[0]
            arguments = words[1:]
            result = operate(operator, arguments)
            if result == None and not top:
                print('Error: {}: unrecognized command!'.format(operator))
            evaluated = True
            return result
        #print('loop ended!')


try:
    code = open(filename).read()
except:
    print('Error! Could not open file: {}.'.format(filename))
    os._exit(0)

lines = code.split('\n')
program = {}

for line in lines:
    #print('evaluating: ' + line)
    if not len(line) == 0 and not line[0] == '#':
        evaluate(line)
