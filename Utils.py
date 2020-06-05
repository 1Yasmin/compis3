import re

class func_Parser:
    def __init__(self):
        self.name= ""
        self.atributos = [] 
        self.lineas = []


def getfun(prod):
    prodl = []
    pointer = 0
    while pointer < len(prod):
        x = re.search("=", prod[0])
        name = prod[slice(0,x.start())]
        pointer += x.start()
        if prod[0].find("<") != 0:
            start = re.search("<", prod[0])
            stop = re.search(">", prod[0])
            attri = prod[0][slice(start.start(), stop.start())]
            attri.strip("return int char")
        prod = prod[slice(stop.start(), len(prod))]
        count = 0
        for line in prod:
            line.strip(" .")
            line.strip("; ")
            line.strip("(.")
            line.strip(".)")
            line.replace("{", "while:")
            line.replace("[", "if")
            prodl.append(line)
            line.strip("ref")
            line.replace("<", "(")
            line.replace(">", ")")
            count += 1
            if line == len(prod):
                s = "return ", line
                prodl.append(s)
            prodl.append(line)
    return name, attri , prodl



def descensoDelGradiente(comptxt):
    f = open("myParser.py", "w")
    prod = []
    txt = comptxt
    cantF = txt.count("=")
    num = 0
    while num < cantF:
        print(num)
        if num == 0:
            x = re.search("=", txt)
            prod.append([txt[slice(0, x.start()+1)]])
            txt = txt[slice(x.start()+1, len(txt))]
            print("x", x)
            num += 1
        else:
            x = re.search("=", txt)
            particion = txt[slice(0,x.start()+1)]
            point = particion.rfind(".")
            #añadir cuerpo de la funcion
            prod[num-1].append(txt[slice(0,point)])
            prod.append([txt[slice(point, x.start() +1)]])
            txt = txt[slice(x.start()+1, len(txt))]
            num += 1
    

        for a in prod:
            name, atri, lin = getfun(a)
            if atri == []:
                s = "def "+ name+ ": \n"
                f.write(s)
            else:
                x = ",".join(atri)
                s = "def "+ str(name)+ "(" +x+"): \n"
                f.write(s)

            for l in lin:
                f.write(l)

    f.close()

