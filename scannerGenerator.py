
from Automata import *
from Thompson import *
from DFA import *
        
def nextState(s,sim,trans):
    for a in trans:
        if ((a[0] == s) and  (sim in a[2])):
            return a[1], 0

    return False, s

def getSimTok(dic):
    simbols = []
    for token in dic: 
        simbols = joinList(simbols, dic[token].symbols)
    return simbols

def lookChar(char_list, ch):
    #print("chq¿ar", char_list,"\n", ch)
    for a in char_list:
        if ch in a:
            return True
    return False

def simulacion(Aut, exp, simbols):
    s = Aut.initial_state[0]
    trans = Aut.transitions
    c = 0
    while(c < len(exp)):
        s, d = nextState(s,exp[c],trans)
        if(s != False):
            c += 1
        else:
            if lookChar(simbols, exp[c]):
                pchar = True
            else:
                pchar = False
            if(d in Aut.final_states):
                    return False, pchar, True, c
            else:
                return False, pchar, False, c
    if(s in Aut.final_states):
        return True, True, True, c
    else:
        return False, False, False, c


def simulacionAutomaton(Aut_dic, except_tokens, exp):
    tok_finales = {}
    simbols = getSimTok(Aut_dic)
    start = 0
    token_test = []
    for a in Aut_dic:
        token_test.append(a)
        tok_finales[a] = []
    print(exp)
    print(tok_finales)   
    tok_count = 0 
    while(start < len(exp)):
        print("New iteration:", start, len(exp))
        if (tok_count < len(token_test)):
            pertenece, chars, fstate, lenC = simulacion(Aut_dic[token_test[tok_count]], exp[slice(start, len(exp))], simbols)
            print("*****Results*****\n", "tok_count",tok_count ,"\npertenece: ", pertenece, "\n chars:", chars, "\n fstate:", fstate, "\n")
            if(pertenece == True):
                print("Easy Pertenece")
                ls = tok_finales[token_test[tok_count]]
                ls.append([exp[slice(start, start+lenC)]])
                tok_finales[token_test[tok_count]] = ls 
                start += lenC
                tok_count = 0
            else:
                #print("la exp:", exp[(start+lenC)])
                #print(chars, fstate)
                if(fstate == True):
                    ls = tok_finales[token_test[tok_count]]
                    ls.append([exp[slice(start, start+lenC)]])
                    tok_finales[token_test[tok_count]] = ls 
                    print("True and True", tok_finales, start, lenC, exp[slice(start, start+lenC)])
                    start += lenC
                    print("*****start****", start)
                    tok_count = 0                    
                if (exp[start+lenC] == "\t" or exp[start+lenC] == "\n"  ):
                    print("With slashes: ", exp[start+lenC+1])
                    start += lenC+1
                    tok_count = 0
                    print("*****start1****", start)
                elif(chars == True and fstate == False):
                    tok_count += 1 
                    print("*****start2****", start, tok_count)
                elif(chars == False and fstate == False):
                    print("Error found")
                    tok_count = 0
                    start += lenC+1
                    print("*****start3****", start)
                
    return tok_finales