# Libraries
from itertools import permutations, combinations, product
import time
import enchant


# Let user type in a list of jumbled up words
def input_jumbled_words():
    # Determine how many jumbled words
    while True:
        try:
            num_words = int(input('How many words would you like to unscramble? '))
            break
        except:
            print('Please only use numbers')

    jumbled_words = []          # Empty list for the jumbled up words
    relevant_positions = {}     # Empty dictionary for the circled positions. Key = jumbled str. Value = list of ints.

    # Get the user inputs of the jumble words
    while len(jumbled_words) < num_words:
        # Have the user input a jumbled string of characters
        jumble_msg = 'Please enter jumbled word ' + str(len(jumbled_words) + 1) + ' of ' + str(num_words) + ': '
        while True:
            scrambled_characters = input(jumble_msg)
            if any(digit.isdigit() for digit in scrambled_characters):
                print('Please only use letters.')
            else:
                break
        jumbled_words.append(scrambled_characters)

        # Have the user input which positions are used for the final phrase
        position_msg = 'Please enter the circled positions for \'' + scrambled_characters + '\' : '
        relevant_pos = [int(x) - 1 for x in list(input(position_msg))]
        relevant_positions.update({scrambled_characters: relevant_pos})

    return jumbled_words, relevant_positions


# Unscramble a set of characters. Returns set of possible words.
def unscramble_word(jumbled_word, word_len):
    d = enchant.Dict("en_US")       # Create PyEnchant dictionary object
    valid_words = set()             # Empty set to hold valid words

    # Split jumbled word into list of jumbled characters
    jumbled_characters = list(jumbled_word)

    # Find all possible permutations of the jumbled characters
    character_permutations = list(permutations(jumbled_characters, word_len))

    # Loop through the options and only keep the ones which are valid words
    for option in character_permutations:
        # Turn list of characters into a string
        word = ''.join(option)

        # Use PyEnchant dictionary object to check if string is a valid word and ignore words matching input
        if d.check(word) and word != jumbled_word:
            valid_words.add(word)

    return list(valid_words)


# Main
def main():
    # Get jumble inputs from user
    jumble, circles = input_jumbled_words()

    # Get all possible words
    unscrambled_words = {}
    for scrambled_word in jumble:
        unscrambled_words.update({scrambled_word: unscramble_word(scrambled_word, len(scrambled_word))})
    print(unscrambled_words)

    # Get the possible solutions by using the combinations of the unscrambled words
    possible_solutions = list(product(*[val for val in unscrambled_words.values()]))
    print(possible_solutions)

    # Save possible letter banks for the phrase as a set of tuples
    letter_bank = set()
    for solution in possible_solutions:
        possible_letter_bank = []
        for index in range(len(solution)):
            for circle in list(circles.values())[index]:
                possible_letter_bank.extend(solution[index][circle])
        letter_bank.add(tuple(possible_letter_bank))
    print(letter_bank)

    # Have the user input the final phrase
    final_phrase_msg = 'Please enter the final phrase format. For unknown words enter the lengths: '
    final_phrase = list(input(final_phrase_msg).split(' '))

    # Attempt to solve the final phrase for each possible letter bank
    eureka = []
    for bank in letter_bank:
        unknown_word_options = []
        final_phrase_options = []
        bk = ''.join(sorted(''.join(bank)))
        # Loop through the list representing the final phrase
        for unknown_word_length in final_phrase:
            # If the element of the list is a digit -- it's a word that needs to constructed from the letter bank
            if unknown_word_length.isdigit():
                # Get all possible n-length words from the letter bank
                possible_words = unscramble_word(bank, int(unknown_word_length))
                unknown_word_options.append(possible_words)

        # Get every possible combination of every possible word
        final_phrase_options.append(list(product(*unknown_word_options)))

        # Only store the proposed answers that match the word bank
        for answer in final_phrase_options:
            for a in answer:
                ans = ''.join(sorted(''.join(a)))
                if ans == bk:
                    eureka.append(a)
                    print(ans)

    print(eureka)


# Let's get it popping
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
