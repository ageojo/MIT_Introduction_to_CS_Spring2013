# 6.00 Problem Set 2
# Name: Amy C. Geojo

# Hangman
#


# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
#

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a dictionary mapping letter counts to lists of valid words of
    that length. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # close the inFile: it's good to close the file when you finish using it!
    inFile.close()

    # wordlist: list of strings
    wordlist = string.split(line)
    word_dict = {}
    for word in wordlist:
        if word_dict.get(len(word)):
            word_dict[len(word)].append(word)
        else:
            word_dict[len(word)] = [word]
    print "  ", len(wordlist), "words loaded."
    return word_dict

def choose_word(word_dict, num_letters):
    """
    word_dict (dict): dictionary mapping integers to lists of words (strings)

    Returns a random word with num_letters letters.
    """
    return random.choice(word_dict[num_letters])

# end of helper code
# -----------------------------------

# load the words into the word_dict variable
# so that it can be accessed from anywhere in the program
word_dict = load_words()

# your code begins here!

""" first list of relevant functions to create"""


def Fill_In_Guessed_Letters(guess, mystery_word, guess_word_list):
    """
    compares each element of mystery_word with guess.
    if guess matches an element in mystery_word, this function returns a list (guess_word_list)
    with the matching element at the same index as in mystery_word.
    note to self: must have guess_word_list as argument
    """
    for i in range(len(mystery_word)):
        if guess == mystery_word[i]:
            guess_word_list[i] = mystery_word[i]
    return guess_word_list


################### END FUNCTIONS ###################
 
num_letters = int(raw_input("Please input the length of the word you want to guess: "))

while num_letters < 2 or num_letters > 10:
    num_letters = int(raw_input("Please input the length of the word you want to guess: "))


mystery_word = choose_word(word_dict, num_letters)  # randomly select word with number of letters specificed by user
print mystery_word

# set number of guesses allowed given word length
Guess_Left = int(len(mystery_word) + len(mystery_word)/3)


# creates a list with as many elements as the mystery word but where each element is a "_"
guess_word_list = []
for i in range(len(mystery_word)):
    guess_word_list.append(" _")


# while loop should run so long as word is not guessed & player has remaining guesses
while Guess_Left > 0:
    
    print "You have " + str(Guess_Left) + " guesses left."       

    guess_in_upper_case = raw_input("Please guess a letter: ")
    guess = guess_in_upper_case.lower()
    
    guess_word_list = Fill_In_Guessed_Letters(guess, mystery_word, guess_word_list) 
    t = ""
    guess_word = t.join(guess_word_list)    #turns list to string
    
    
    if guess in mystery_word: # check to see if guess (user input) is in chosen_word
        print "Good guess: " + str(guess_word)
        if mystery_word == guess_word:  # check if entire word has been guessed
            break
    else:
        print "Oops! That letter is not in my word: " + str(guess_word)
        Guess_Left = Guess_Left - 1
       

if mystery_word == guess_word: 
    print "Congratulations, you won!"
else:
    print "Game over. You lose!"
    print "The correct word is " + "'" + str(mystery_word) + "'"
    
    

        
 
