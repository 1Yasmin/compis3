import re
from scannerGenerator import *
from Proyecto1 import *
from Utils import *

file_name = input("Ingrese el nombre del archivo: ")

f = open(file_name, "rt")
fcontent = f.read()
f.close()

"""
fcontent = fcontent.split("\n")
enter = 0
print(fcontent)
for a in fcontent:
    enter = enter + fcontent.count("\n")

while enter != 0:
    fcontent.remove("\n")
    enter =- 1

print(fcontent)

"""

def process(dic, val):
    if(val.find("+") != -1):
        values = val.split("+")
        for a in values:
            ind = values.index(a)
            values[ind] = a.strip()
    elif(val.find("-") != -1):
        values = val.split("-")
        for a in values:
            ind = values.index(a)
            values[ind] = a.strip()
    else: 
        values = [val]
    #print(values)
    all_val = []
    for v in values:
        if (v in dic):
            #TODO: joinlist
            all_val.append(dic.get(v))
        if (v.find("CHR") != -1):
            start = val.index("(")
            end = val.index(")")
            num = int(val[start+1:end])
            all_val.append(chr(num))
        elif(v.find("a\"..\"z") != -1):
            all_val.append(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        elif(v.find("\"A\"..\"Z\"") != -1):
            all_val.append(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
        else:
            return values[0].strip("\"\"")
        
    return all_val

def diccionario(content):
    dic = {}
    for a in content:
        if(a != ""):
            key_val = a.split('=')
            #print(key_val)
            key = key_val[0].strip()
            val = key_val[1]
            valtemp = val.strip(" .")
            #print(valtemp)
            valtemp = process(dic, valtemp)
            dic[key] = valtemp
    return dic

try: 
    x1 = fcontent.find("COMPILER")
    x2 = fcontent.find("CHARACTERS")
    x3 = fcontent.find("KEYWORDS")
    x4 = fcontent.find("TOKENS")
    x5 = fcontent.find("PRODUCTIONS")
    x6 = fcontent.find("END")
    x7 = fcontent.count("/**")

except:
    pass

print("************************************************************")
COMP = fcontent[slice(x1,x2)].split("\n")
COMPI = COMP[0].split(" ")
COMPILER = {}
COMPILER["name"] = COMPI[1]
print(COMPILER)

print("************************************************************")
CHARACTERS = fcontent[slice(x2,x3)].split("\n")
CHARACTERS.remove(CHARACTERS[0])
CHARACTERS = diccionario(CHARACTERS)
print(CHARACTERS)

print("************************************************************")
#print(fcontent[slice(x3,x4)])
KEYWORDS = fcontent[slice(x3,x4)].split("\n")
KEYWORDS.remove(KEYWORDS[0])
KEYWORDS = diccionario(KEYWORDS)
print(KEYWORDS)

print("************************************************************")
#print(fcontent[slice(x4,x5)])
TOKENS = fcontent[slice(x4,x5)].split("\n")
TOKENS.remove(TOKENS[0])
TOKENS = diccionario(TOKENS)
print(TOKENS)

print("************************************************************")
#print(fcontent[slice(x4,x5)])
PRODUCTIONS = fcontent[slice(x5+11,x6)]
# Proyecto 3
descensoDelGradiente(PRODUCTIONS)

print("************************************************************")
END_txt = fcontent[slice(x1,x2)].split("\n")
END_name = END_txt[0].split(" ")
END = {}
END["name"] = END_name[1]
print(END)

def token_to_regex(tok):
    regex = tok.replace("{", "(")
    regex = regex.replace("}", ")*")
    return regex

#Obtener los Tokens con EXCEPT KEYWORDS
except_tokens = []
for tok in TOKENS:
    temp = TOKENS[tok]
    if ("EXCEPT KEYWORDS" in temp):
        temp = TOKENS[tok].strip(" EXCEPT KEYWORDS")
        TOKENS[tok] = temp
        except_tokens.append(tok)
    
#print(except_tokens)
#print("***", TOKENS)

#Characters 
char_names =[]
for name in CHARACTERS:
    char_names.append(name)

# Generar un automata por token
aut_dic = {}
for tok in TOKENS:
    temp = TOKENS[tok]
    regex = token_to_regex(temp)
    #print(regex)
    #Enviar al proyecto 1
    aut_tok = proyecto(regex, char_names)
    aut_dic[tok] = aut_tok

#Modificar los characteres en el autómata
for aut in aut_dic:
    simbol = []
    for name in CHARACTERS:
        start_sim = aut_dic[aut].symbols
        if name in start_sim:
            simbol.append(CHARACTERS[name])
            aut_dic[aut].set_trans_symbol(name, CHARACTERS)
    aut_dic[aut].set_symbols(simbol)


for aut in aut_dic:
    name = "AFD"+aut
    # Guardar AFD en un archivo
    file = open(name+".txt", "w")
    file.write("Estado inicial:  "+ str(aut_dic[aut].initial_state)+"\n")
    file.write("Estado(s) de aceptación:  "+ str(aut_dic[aut].final_states)+"\n")
    file.write("Estados:  "+ str(aut_dic[aut].states)+"\n")
    file.write("Símbolos:  "+ str(aut_dic[aut].symbols)+"\n")
    file.write("Transiciones:  "+ str(aut_dic[aut].transitions)+"\n")
    file.close()
    # Graficar AFD
    #graficar(aut_dic[aut].final_states, aut_dic[aut].transitions, name)
    #print("Para DFA:", simulacionAutomataDFA(aut_dic[aut], "hola"))
    #print("Para DFA:", simulacionAutomataDFA(aut_dic[aut], "hola12jk"))
    #print("Para DFA:", simulacionAutomataDFA(aut_dic[aut], "4"))

# Creación del automaton
# array except_tokens

#print(aut_dic)
f = open("test.txt", "rt")
txt = f.read()
f.close()
#txt = "holamun25\n"
tokens_found = simulacionAutomaton(aut_dic, except_tokens, txt)
print(tokens_found)





