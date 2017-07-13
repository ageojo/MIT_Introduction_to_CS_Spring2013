# Problem Set 4C
# Name: Amy C. Geojo



# Helper Functions #
def isInt(w):
    try:
        ret = int(w)
        return True
    except ValueError:
        return False

#end helper functions
    

def printExpr(elist):
    if elist == []:
        return ("", [])

    elif isInt(elist[0]):
        return (elist[0], elist[1:])

    elif elist[0] == "+":
        k, v = printExpr(elist[1:])
        k2, v2 = printExpr(v)
        return "(" + k + elist[0] + k2 + ")", v2
    elif elist[0] == "*":
        k, v = printExpr(elist[1:])
        k2, v2 = printExpr(v)
        return "(" + k + elist[0] + k2 + ")", v2
    



def evalExpr(elist):
    if elist == []:
        return (0, [])

    elif isInt(elist[0]):
        return (int(elist[0]), elist[1:])

    elif elist[0] == "+":
        k, v = evalExpr(elist[1:])
        k2, v2 = evalExpr(v)
        return (int(k) + int(k2)), v2
    else:
        k, v = evalExpr(elist[1:])
        k2, v2 = evalExpr(v)
        return (int(k) * int(k2)), v2





# -----------------------------
# Testing

def testerPrinter(printer):
    def check(instr, expected):
        rv, rest = printer(instr)
        if( rv != expected ):
            print 'Test for "' + str(instr) + '" failed returned ' + str(rv) + ' instead of ' + str(expected)
            return False
        print str(instr) + ' = ' + str(rv)
        return True
    
    rv = True
    rv = check(['+', '5', '9'], '(5+9)') and rv
    rv = check(['+', '5', '10'], '(5+10)') and rv 
    rv = check(['+', '8', '*', '5', '2'], '(8+(5*2))') and rv    
        
    #Add more of your own tests here.
    rv = check(["*", "5", "9"], '(5*9)') and rv
    rv = check(['+', '5', '+', '3', '10'], '(5+(3+10))',) and rv
    rv = check(['*', '5', '*', '3', '10'], '(5*(3*10))',) and rv
    rv = check([], '') and rv
    rv = check(["*", "0", "9"], '(0*9)')  and rv
    rv = check(['+', '*', '1', '5', '10'], '((1*5)+10)',) and rv
    rv = check(['+', '*', '+', '1', '5', '10', '4'], '(((1+5)*10)+4)',) and rv 
    
    
    if(rv):
        print 'All tests passed!'


def testerEvaluator(evaluator):
    def check(instr, expected):
        rv, rest = evaluator(instr)
        if( rv != expected ):
            print 'Test for "' + str(instr) + '" failed returned ' + str(rv) + ' instead of ' + str(expected)
            return False
        print str(instr) + ' = ' + str(rv)
        return True
    
    rv = True
    rv = check(['+', '5', '9'], 14) and rv
    rv = check(['+', '5', '10'], 15) and rv 
    rv = check(['+', '8', '*', '5', '2'], 18) and rv    
        
    #Add more of your own tests here.
    rv = check(["*", "5", "9"], 45) and rv
    rv = check(['+', '5', '+', '3', '10'], 18) and rv
    rv = check(['*', '5', '*', '3', '10'], 150) and rv
    rv = check([], 0) and rv
    rv = check(["*", "0", "9"], 0)  and rv
    rv = check(['+', '*', '1', '5', '10'], 15,) and rv
    rv = check(['+', '*', '+', '1', '5', '10', '4'], 64,) and rv 
 
    
    
    
    if(rv):
        print 'All tests passed!'

testerPrinter(printExpr)
testerEvaluator(evalExpr)







