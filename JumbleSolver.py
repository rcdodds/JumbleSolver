# Libraries
from itertools import permutations, combinations, product
import enchant


# Let user type in a list of jumbled up words
def input_jumbled_words():
    num_words = int(input('How many words would you like to unscramble? '))
    jumbled_words = []
    relevant_positions = {}

    # Get the words and circled positions from the user
    while len(jumbled_words) < num_words:
        # Have the user input a jumbled string of characters
        msg = 'Please enter jumbled word ' + str(len(jumbled_words) + 1) + ' of ' + str(num_words) + ': '
        scrambled_characters = input(msg)
        jumbled_words.append(scrambled_characters)

        # Have the user input which positions are used for the final phrase
        message = 'Please enter the circled positions (comma-delimited) for \'' + scrambled_characters + '\' : '
        relevant_pos = [int(x) - 1 for x in list(input(message))]
        relevant_positions.update({scrambled_characters: relevant_pos})

    return jumbled_words, relevant_positions


# Unscramble a set of characters. Returns set of possible words.
def unscramble_word(jumbled_word):
    d = enchant.Dict("en_US")       # Create PyEnchant dictionary object
    valid_words = set()             # Empty set to hold valid words

    # Split jumbled word into list of jumbled characters
    jumbled_characters = list(jumbled_word)

    # Find all possible permutations of the jumbled characters
    character_permutations = list(permutations(jumbled_characters, len(jumbled_characters)))

    # Loop through the options and only keep the ones which are valid words
    for option in character_permutations:
        # Turn list of characters into a string
        word = ''.join(option)

        # Use PyEnchant dictionary object to check if string is a valid word
        if d.check(word):
            valid_words.add(word)

    return list(valid_words)


# Main
def main():

    # Get jumble inputs from user
    jumble, circles = input_jumbled_words()

    # Get all possible words
    unscrambled_words = {}
    for scrambled_word in jumble:
        unscrambled_words.update({scrambled_word: unscramble_word(scrambled_word)})
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


# Let's get it popping
if __name__ == '__main__':
    main()
