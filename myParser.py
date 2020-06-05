def Expr():
    Stat()

def Stat():
    value = 0
	Expression(value)	
    print(value)

def Expression(result):
    result1, result2
	Term(result1)
    while:
        Term (result2)
        result1 += result2
	   |"-"Term(result2)
       result1-=result2
	
    return result=result1

def Term(result)
    result1,result2 
	Factor(result1)
	while:
        "*"Factor(result2)
        result1*=result2
	   | "/"Factor(result2)	
       result1/=result2
    return result=result1

def Factor(result)
    signo=1
	if: 
        "-"signo = -1
	Number(result) | Expression(result)
    return result*=signo

def Number(result)
   number result = Parse(lastToken.Value)