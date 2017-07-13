# Problem Set 4A
# Name: Amy C. Geojo


def x_ian(x, word):
    '''
        Given a string x, returns True if all the letters in x are
        contained in word in the same order as they appear in x.
        
        x: a string
        word: a string
        returns: True if word is x_ian, False otherwise
    '''

    # your code here
    #pass
    
    word = word.lower()
    x = x.lower()


    if len(x) == 0:
        return True
    
    elif len(word) < len(x):
        return False

    elif x[0] == word[0]:
        return x_ian(x[1:], word[1:])
    else:
        return x_ian(x, word[1:])
  


# -----------------------------
# Testing

def testerFunction(checker):
    def check(instr, expected):
        if checker(instr[0], instr[1]) != expected:
            print 'Test for "' + str(instr) + '" failed '
            return False
        return True
    #The following should be true
    rv = True
    rv = check(('srini', 'histrionic'), True) and rv
    rv = check(('dina', 'dinosaur'), True) and rv    
    #The following should be false
    rv = check(('john', 'mahjong'), False) and rv
    rv = check(('pangus', 'angus'), False) and rv

    #Add more of your own tests here.
    rv = check(('bar', ""), False) and rv
    rv = check(("", ""), True) and rv
    rv = check(("", 'bar'), True) and rv    
    rv = check(('foo', "oof"), False) and rv    
    rv = check(('foof', 'foo'), False) and rv      
    rv = check(('fo.fo', 'fofofo'), False) and rv  
    rv = check(("don't", "dontt"), False) and rv 
    rv = check(('Furth', 'fruereTH'), True) and rv  


    
    if(rv):
        print 'All tests passed!'


testerFunction(x_ian)


