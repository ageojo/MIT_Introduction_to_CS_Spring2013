# Problem Set 4B
# Name: Amy C. Geojo


# ----------------------------
# Helper functions

def ignoreChar(c):
    '''Check if a character c should be ignored.
        Opening and closing brackets and parenthesis should not be ignored.
    '''
    if c in ['(', ')']:
        return False
    else:
        return True

# end of helper functions
# ----------------------------

def checkParenthesis(word):
    '''Check if a string is properly parenthesized.
    The function returns a boolean True or False depending on
    whether the word is properly parenthesized or not.
    Base case:
        Words of length zero are always properly parenthesized.
    Recursive case 1:
        If the first letter in a word is not a parenthesis,
        the word is properly parenthesized if the rest of the word is properly parenthesized
    Recursive case 2:
        If the first letter is  '(', call completeRound
        to find a matching ')' and check parenthesization along the way.
        If it failed to find a match, return False. Otherwise, check if the rest of the word is correctly parenthesized. 
    '''

    #your code here
    if word == "":
        return True
    
    elif ignoreChar(word[0]):
        return checkParenthesis(word[1:])
    
    elif word[0] == "(":
        k, v= completeRound(word[1:])
        if k:
            return checkParenthesis(v)
        else:
            return False
    else:
        return False


      
""" should be able to assume that completeRound(word) -- will return a tuple (bool, word);
 checkParenthesis only takes word as argument, so it can only take index 1 of completeRound to continue to
 check parenthesis on whatever is left in the word
 however there's no need to check the rest of the word if completeRound fails to find a match-- checkParenthesis should at
 that point return False
 """


    


def completeRound(word):
    '''
        The function assumes that word contains the text immediately
        after an opening parenthesis, not including the original
        opening parenthesis. It will find a matching closing parenthesis
        and will check parenthesization between the beginning of word and the matching closing parenthesis.
        
        The function returns a pair (b, rest), where b is a boolean describing
        whether it encountered an error, and rest is the rest of the word
        after the matching closing parenthesis.
        Base case 1:
            If the word is of length zero, it means there was no text after
            the opening parenthesis. This is an error, so the function should
            return (False, something). It doesn't matter what something is,
            because it should be ignored.

        Base case 2:
            If the first character is a closing round parenthesis ')', we have found a match,
            so we can return (True, rest), where rest is the rest of t he word after the closing parenthesis.
            
        Recursive case 1:
            If the first letter is not a parenthesis, it can be ignored.
            The return values should be the same as if the function had been called with word[1:] instead of with word.
        Recursive case 2:
            Can you figure out the details of what happens when the first
            character is an opening parenthesis '('?
            Hint: we need to find a match for this new open parenthesis before
            we can continue looking for a match for the current open parenthesis
            in the rest of the word.
    '''

    #your code here
    if word == "":
        return (False, "")
    
    elif word[0] == ")":
        return (True, word[1:])
    
    elif ignoreChar(word[0]):
        return completeRound(word[1:])
    
    else:
        k, v = completeRound(word[1:])
        if k:
            return completeRound(v)
        else:
            return (False, "")



# -----------------------------
# Testing

def testerFunction(checker):
    def check(instr, expected):
        if checker(instr) != expected:
            print 'Test for "' + instr + '" failed '
            return False
        return True
    #The following should be true
    rv = True
    rv = check('( x (y + z ) w(a b c))(t + x(z))', True) and rv
    rv = check('((()() )(  (u)(  x )))', True) and rv    
    #The following should be false
    rv = check(')(())(', False) and rv
    rv = check('(x + y (z)', False) and rv
    #Add more of your own tests here.
    rv = check('(', False) and rv
    rv = check(')', False) and rv
    rv = check('', True) and rv
    rv = check('abc', True) and rv
    
    if(rv):
        print 'All tests passed!'


testerFunction(checkParenthesis)
