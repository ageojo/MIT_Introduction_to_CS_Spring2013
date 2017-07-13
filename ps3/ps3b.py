# Problem Set 3B
# Name: Amy C. Geojo



from ps3a import *
import time
from perm import *


# Problem #6: Computer chooses a word


def comp_choose_word(hand, word_list):
    """
    Given a hand and a word_dict, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all possible 
    permutations of lengths 1 to HAND_SIZE.

    If all possible permutations are not in word_list, return None.

    hand: dictionary (string -> int)
    word_list: list (string)
    returns: string or None
    """
 
    permutation_list = []

    
    for n in range(1, HAND_SIZE + 1):
            permutation_list += get_perms(hand, n)
            
        
    maxScore = 0
    bestWord = ""

    for w in permutation_list:
        if w in word_list:
            if maxScore < get_word_score(w, HAND_SIZE):
                maxScore = get_word_score(w, HAND_SIZE)
                bestWord = w
                
                
    return bestWord
    
 
#
# Problem #7: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
    Allows the computer to play the given hand, following the same procedure
    as play_hand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. comp_choose_word returns None).
 
    hand: dictionary (string -> int)
    word_list: list (string)
    """

 
    oldHand = hand
    handLength = calculate_handlen(hand)  
    totalScore = 0
 
    word = ""
    while handLength > 0: 
        print "Current Hand: "
        display_hand(oldHand)
        
        word = comp_choose_word(oldHand, word_list)
        
        if word == "":
            break
        
        else: 
            wordScore = get_word_score(word, handLength)
            totalScore += wordScore

            print word + " earned " + str(wordScore) + " points." 
            print "Total score: " + str(totalScore)

            oldHand = update_hand(oldHand, word)
            handLength = calculate_handlen(oldHand)
         
        
    print "Game over! Your total score for this round was: " + str(totalScore)
    return hand

    

    
#
# Problem #8: Playing a game
#
#
def play_game(word_list, hand):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using play_hand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using comp_play_hand.

    4) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """

       
    playerChoice = str(raw_input("Enter 'n' to play a new hand. Enter 'r' to play the last hand. Enter 'e' to exit the game: "))
    playerChoice = playerChoice.lower()
    
    while playerChoice not in ['n', 'r', 'e']:
        playerChoice = str(raw_input("That is not a valid response. Enter 'n' to play a new hand. Enter 'r' to play the last hand. Enter 'e' to exit the game: "))

    if playerChoice == 'e':
        return

    if playerChoice == 'n':
        hand = deal_hand(HAND_SIZE)

    elif playerChoice == 'r':
        hand = hand
    
    decide_turn = str(raw_input("Enter 'u' to play the hand or 'c' to let the computer play: " ))
    decide_turn = decide_turn.lower()

    while decide_turn not in ['c', 'u']:
        decide_turn = str(raw_input("That is not a valid response. Enter 'u' to play the current hand or 'c' to let the computer play: "))


    if decide_turn == 'c':
        comp_play_hand(hand, word_list)

    elif decide_turn == 'u':
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

    print "Goodbye!"
