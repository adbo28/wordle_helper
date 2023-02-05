
from collections import Counter

from util import load_words, valid, update_freq, calc_score, get_char_scores


###########################################################
def main(pattern, misplaced_chars, forbidden_chars):
    """
    pattern - five char string consisting of ALPHABET_FULL or other
    characters such as '-'.
    misplaced_chars - list of five non-empty character sets consisting of ALPHABET or
    other character such as '-'. X in char_combination[i] means that the
    hidden word must contain X, but not on position i.
    forbiden_chars - must not appear in the word
    Example: pattern = 'sp---' and miplaced_chars = ['-','-','-','i','c'] and 
    forbidden_chars = 'xqs' means that the hidden word starts with 'sp' and contains 'i' 
    and 'c' whereas 'i' must not be on 4-th position and 'c' must not be on 5-th
    and the hidden word does not contain 'xqs' on any position"""

    # a list of five counters; each counter counts occurences of a given 
    # character at the particular place; only characters from ALPHABET are used
    char_freq = [Counter(), Counter(), Counter(), Counter(), Counter()]

    # calculate character frequencies
    words = load_words()
    valid_words = []
    for w in words:
        if valid(w, pattern, misplaced_chars, forbidden_chars):
            valid_words.append(w)
            update_freq(w, char_freq)

    # find the best matching word
    matching_words = Counter()
    best_word = ''
    best_score = 0
    for w in valid_words:
        score = calc_score(w, char_freq)
        matching_words[w] = score
        if score > best_score:
            best_word = w
            best_score = score

    # output
    print('----')
    print(f'valid words: {len(matching_words)}')
    print(best_word)
    for(w,score) in matching_words.most_common(min(len(matching_words), 10)):
        print(f'{w}, freq:{get_char_scores(w, char_freq)}')

    for i, cntr in enumerate(char_freq):
        print(f'position {i}: {cntr.most_common(5)}')



###########################################################
def test_valid():

    t = [
        ('hrnec', '-----', '- - - - -', '', True), 
        ('hrnec', 'b----', '- - - - -', '', False), 
        ('hrnec', '-rn--', 'efg - - - -', '', False), 
        ('hrnec', 'h----', '- - - - -', '', True), 
        ('hrnec', 'h----', 'nec - - - -', '', True),
        ('hrnec', 'h----', '- nec - - -', '', True),
        ('padák', 'p--a-', '- - a - -', '', True),
        ('pedál', 'p--a-', '- - a - -', '', False),
        ('pedál', 'p--a-', '- - a - -', 'k', False),
        ('padák', 'p--a-', '- - a - -', 'k', False),
        ('aréna', '---na', '- ae - - -', '', True),
    ]

    for (word, pattern, misplaced_chars, forbidden_chars, expected) in t:
        res = valid(word, pattern, misplaced_chars.split(), forbidden_chars, report_errors=True)
        if expected == res:
            print(f'word:{word}, pattern:{pattern}, res:{res}')
        else:
            print(f'[TEST FAILED] word:{word}, pattern:{pattern}, res:{res}')
        print()



###########################################################

main('----n',['-','-','-','-','-'], '')

# test_valid()

