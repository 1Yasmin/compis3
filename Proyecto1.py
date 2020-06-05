"""
   Entrada de datos
   *** Implementación de Thompson

   Construcción de NFA --> Simulación (si o no de una cadena w)
   
   Contrucción de subconjuntos
        Tabla con:    NFA | DFA  | Variables....
    Construcción de AFD dada r
    Graficar el AFD

    Simulación de AFD --> (si o no de una cadena w)
    
    Extra:  Minimización de los AF

    Imprimir para cada AF generado a partir de r, 
        -un SÍ o NO según si la cadena pertenece al lenguaje
    Tiempo que tarda cada AF en realizar la validacion de una cadena
    -Generar archivo por cada AF con 
            -Estados, simbolos, inicio, acepación, transcisión
"""

import os
import numpy as np
from copy import deepcopy
import time
from graphviz import Digraph
from Thompson import Thompson
from DFA import createDFA
from graph import graficar 
from D_AFD import D_DFA
import copy



class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]
        
def infixTopostfix(exp, characters):

    mod = exp[0]
    for i in range(1,len(exp)):
        if( (((exp[i] in characters) and exp[i-1] != '(') or exp[i] == '(') and (exp[i-1] != '|' or exp[i-1] == ')') ):
            mod += '.'+exp[i]
        else:
            mod += exp[i]

    regex = mod
    prec = {}
    prec["?"] = 4
    prec["*"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
    tokens = list(regex)
    output = []
    stack = Stack()
    for token in tokens:
        if (token.isalpha() or token.isdigit() or token == ' '):
            output.append(token)
        elif (token == '('):
            stack.push(token)
        elif (token == ')'):
            top = stack.pop()
            while(top != '('):
                output.append(top)
                top = stack.pop()
        else:
            while (not stack.isEmpty()) and (prec[stack.peek()] >= prec[token]):
                  output.append(stack.pop())
            stack.push(token)
    while(not stack.isEmpty()):
        output.append(stack.pop())
    
    return ''.join(output)

def proyecto(exp, characters):
    regex = ""
    for v in exp:
        if v == "+" or v == "?":
            if(exp[exp.index(v)-1] == ")"):
                inicio = exp.index(v)-1
                pos = exp[exp.index(v)-1]
                while (pos != "("):
                    pos = exp[inicio]
                    inicio -= 1
                values = exp[inicio+1:exp.index(v)]
                if (v == "+"):
                    new_regex = exp[:exp.index(v)] + values + "*"+ exp[exp.index(v)+1:] 
                elif (v == "?"):
                    new_regex = exp[:exp.index(v)-(len(values)-1)] + values + "|3)"+ exp[exp.index(v)+1:] 
                exp = new_regex
            else:
                val = exp[exp.index(v)-1]
                if (v == "+"):
                    new_regex = exp[:exp.index(v)] + val + "*"+ exp[exp.index(v)+1:]  
                elif(v == "?"):
                    new_regex = exp[:exp.index(v)-1] +"(" + exp[exp.index(v)-1] + "|3)"+ exp[exp.index(v)+1:]
                exp = new_regex
    
    if(("+" not in exp) and ("?" not in exp)):
        regex = exp

    postfix = infixTopostfix(regex, characters)
    print("La postfix regex: ", postfix)
    
    #print(postfix)
    #cadena de tokens
    tokens = []
    while len(postfix) != 0:
        if (postfix[0] == "|" or postfix[0] == "*" or postfix[0] == "."):
            tokens.append(postfix[0])
            postfix = postfix[slice(1,len(postfix))]
        else:
            for a in characters:
                if (postfix.find(a) != -1):
                    postfix = postfix[slice(len(a), len(postfix))]
                    tokens.append(str(a))
                    break
    print("tokens: ", tokens)
    
    
    #Contrucción del NFA 
    countState = 0
    if(len(tokens) == 1):
        tokens, countState = Thompson(tokens, countState)
    while(len(tokens) > 1):
        tokens, countState = Thompson(tokens, countState)

    # Automata generado
    Aut = tokens[0]
    # Del AFN a AFD
    AFD = createDFA(Aut)
    
    return AFD
    """
    w = input("Ingrese cadena que desea validar: ")
    print("Para NFA:", simulacionAutomataNFA(Aut, w))
    print("Para DFA:", simulacionAutomataDFA(AFD, w))
    #print("Para DFA Directo:",simulacionAutomata(D_DFA_Aut, w))
    """