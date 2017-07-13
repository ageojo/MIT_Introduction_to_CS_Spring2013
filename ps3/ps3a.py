# Problem Set 3A
# Name: Amy C. Geojo

# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#

import random
import string
import math
import copy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}



# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist



def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 30 points if all n
    letters are used on the first go.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """

    wordScore = 0
    letterFreq = get_frequency_dict(word)
    for key in letterFreq.keys():
        if key in SCRABBLE_LETTER_VALUES.keys():
            wordScore = SCRABBLE_LETTER_VALUES[key]*letterFreq[key] + wordScore
    wordScore = wordScore*len(word)
    if len(word) == n:
        wordScore += 30
    return wordScore




# Problem #2: Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line




#
# Problem #2: Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand



#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    letterFreq = get_frequency_dict(word)
    count = 0
    newHand = {}
    newHand= copy.copy(hand)
    for key in letterFreq.keys():       
        if key in newHand.keys():
            newHand[key] -= letterFreq[key]     # subtracting letters in word from hand; if use 1 or 2 'p' want to keep 1 'p'
            if newHand[key] == 0:               # delete entries in newHand where key value = 0
                del newHand[key]
    return newHand



#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """


    def word_in_hand(wordFreq, newHand):
        wordFreq = get_frequency_dict(word)
        for key in wordFreq:
           if key in newHand and wordFreq[key] <= newHand[key]:
                wordFreq[key] = 0
           else:
               return False
        if sum(wordFreq.values()) == 0:
            return True
        else:
            return False
        
    return word in word_list and word_in_hand(word, hand)




#
# Problem #4: Playing a hand
#

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    handLength = []
    for k in hand:
        handLength.append(hand[k])    
    return sum(handLength)
# return sum(hand.values())    #didn't work before but i've checked it since and now it does. 


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """

    oldHand = hand
    handLength = calculate_handlen(hand)  
    totalScore = 0

    word = ""
    while handLength > 0: 
        print "Current Hand: "
        display_hand(oldHand)
        
        word = str(raw_input("Enter word, or a '.' to indicate that you are finished: "))
        if word == '.':
            break
        if is_valid_word(word, oldHand, word_list):
            wordScore = get_word_score(word, handLength)
            totalScore += wordScore

            print word + " earned " + str(wordScore) + " points." 
            print "Total score: " + str(totalScore)

            oldHand = update_hand(oldHand, word)
            handLength = calculate_handlen(oldHand)
         
        else:
            print "Sorry! That's not a word. Please try again. Your current score is: " + str(totalScore)
            

        
    print "Game over! Your total score for this round was: " + str(totalScore)
    return hand




#
# Problem #5: Playing a game
# 

def play_game(word_list, hand):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, ask them again.
 
    2) When done playing the hand, repeat from step 1    
    """
     
    
    playerChoice = str(raw_input("Enter 'n' to play a new hand. Enter 'r' to play the last hand. Enter 'e' to exit the game: "))
    playerChoice = playerChoice.lower()
    
    while playerChoice not in ['n', 'r', 'e']:
        playerChoice = str(raw_input("That is not a valid response. Enter 'n' to play a new hand. Enter 'r' to play the last hand. Enter 'e' to exit the game: "))

    if playerChoice == 'e':
        return

    elif playerChoice == 'n':    
       hand = deal_hand(HAND_SIZE)
       hand = play_hand(hand, word_list)

    elif playerChoice == 'r':
        play_hand(hand, word_list)
    
    hand = hand
    
    return play_game(word_list, hand)
        
            

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    hand = deal_hand(HAND_SIZE)
    play_game(word_list, hand)
