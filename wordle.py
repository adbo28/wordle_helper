
from collections import Counter



ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_FULL =     'aábcčdďeěéfghiíjklmnňoópqrřsštťuůúvwxyýzž'
ALPHABET_MAPPING =  'aabccddeeefghiijklmnnoopqrrssttuuuvwxyyzz'

FILENAME = 'slovnik5.txt'
# FILENAME = 'slovnik_test.txt'



###########################################################
def load_words():
    """Load all possible words from a file"""
    words = []

    with open(FILENAME, 'r', encoding='UTF-8') as file:
        for word in file:
            words.append(word.strip())

    return words


###########################################################
def replace_special_chars(word):
    word2 = ''
    for c in word:
        i = ALPHABET_FULL.find(c)
        word2 += ALPHABET_MAPPING[i]
    return word2


###########################################################
def valid(word, pattern, misplaced_chars, forbidden_chars, report_errors = False):

    # print(f'w:{word}, pt:{pattern}, misplaced:{misplaced_chars}, forbidden:{forbidden_chars}')

    # check whether pattern is valid
    if (len(pattern) != 5):
        print(f'Pattern not valid; first word ({pattern}) must have five chars')
        return False
    if (len(misplaced_chars) != 5):
        print(f'Pattern not valid; it contains {len(misplaced_chars)} instead of 6')
        return False

    # transform word to a version with special Czech characters replaced
    word2 = replace_special_chars(word)

    # check the first word for right characters
    indices_wrong = [i for i in range(5) if pattern[i] in ALPHABET_FULL and pattern[i] != word2[i]]
    if len(indices_wrong):
        if report_errors:
            print(f'false type 1 (indices_wrong: {indices_wrong})')
        return False

    # check that word does not contain char from p[i+1] on place i
    for i in range(5):
        if pattern[i] not in ALPHABET_FULL:
            # only checked if p[i+1] is relevant, i.e. if the character on the given place is not known yet
            w = misplaced_chars[i]
            indices_wrong = [c for c in w if word[i] == c]
            if len(indices_wrong):
                if report_errors:
                    print(f'false type 2 (indices_wrong: {indices_wrong})')
                return False

    # check that all characters from p[i+1] are in word on other places than those covered by th
    represented_chars = set([c for c in ''.join(misplaced_chars) if c in ALPHABET_FULL])
    remaining_chars = set([c for c,rc in zip(word, pattern) if c != rc])
    if not represented_chars.issubset(remaining_chars):
        if report_errors:
            print(f'false type 3 (rep_chars:{"".join(represented_chars)} is not subset of rem_chars:{"".join(remaining_chars)})')
        return False

    # check that the word does not contain forbidden characters
    word_chars = set(word)
    if len(set(forbidden_chars).intersection(word_chars)):
        if report_errors:
            print(f'false type 4 (word contains forbidden chars:{"".join(forbidden_chars)}')
        return False

    return True



###########################################################
def get_char_scores(word, char_freq):
    """Returns a list of give numbers. X on i-th position means that 
    there are x words with the char word[i] on i-th position.
    I.e. for word = 'thumb' a list [421,...] means that there are 10 words
    starting with a t."""
    res = []
    word2 = replace_special_chars(word)
    for c, cntr in zip(word2, char_freq):
        res.append(cntr[c])
    return res


###########################################################
def calc_score(word, char_freq):
    return sum([x**2 for x in get_char_scores(word, char_freq)])


###########################################################
def update_freq(word, char_freq):
    word2 = replace_special_chars(word)
    for c, cntr in zip(word2, char_freq):
        cntr[c] += 1


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

    char_freq = [Counter(), Counter(), Counter(), Counter(), Counter()]
    # a list of five counters; each counter counts occurences of a given 
    # character at the particular place; only characters from ALPHABET are used

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
    for w in words:
        score = calc_score(w, char_freq)
        matching_words[w] = score
        if score > best_score:
            best_word = w
            best_score = score

    # output
    print(f'valid words: {len(matching_words)}')
    print(best_word)
    print()
    for(w,score) in matching_words.most_common(10):
        print(f'{w}, freq:{get_char_scores(w, char_freq)}')




###########################################################
def test_valid():

    # t = [('hrnec', '-----', '- - - - -', True), ('hrnec', 'b---- - - - - -', False), ('hrnec', '-rn-- efg - - - -', False), 
    #      ('hrnec', 'h---- - - - - -', True), ('hrnec', 'h---- nec - - - -', True), ('hrnec', 'h---- - nec - - -', True),
    #      ('padák', 'p--a- - - a - -', True), ('pedál', 'p--a- - - a - -', False)] 

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
    ]

    for (word, pattern, misplaced_chars, forbidden_chars, expected) in t:
        res = valid(word, pattern, misplaced_chars.split(), forbidden_chars)
        if expected == res:
            print(f'word:{word}, pattern:{pattern}, res:{res}')
        else:
            print(f'[TEST FAILED] word:{word}, pattern:{pattern}, res:{res}')
        print()



###########################################################

main('po---',['-','a','-','e','-'], 'xbe')
main('po---',['-','-','-','-','-'], 'stk')

# test_valid()

