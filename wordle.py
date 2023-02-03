
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
def valid(word, pattern):

    p = pattern.split()

    # print(f'w:{word}, pt:{pattern}')

    # check whether pattern is valid
    if (len(p[0]) != 5):
        print(f'Pattern not valid; first word ({p[0]}) must have five chars')
        return False
    if (len(p) != 6):
        print(f'Pattern not valid; it contains {len(p)} instead of 6')
        return False

    # transform word to a version with special Czech characters replaced
    word2 = replace_special_chars(word)

    # check the first word for right characters
    right_chars = p[0]
    indices_wrong = [i for i in range(5) if right_chars[i] in ALPHABET_FULL and right_chars[i] != word2[i]]
    if len(indices_wrong):
        # print(f'false type 1 (indices_wrong: {indices_wrong})')
        return False

    # check that word does not contain char from p[i+1] on place i
    for i in range(5):
        if right_chars[i] not in ALPHABET_FULL:
            # only checked if p[i+1] is relevant, i.e. if the character on the given place is not known yet
            w = p[i+1]
            indices_wrong = [c for c in w if word[i] == c]
            if len(indices_wrong):
                # print(f'false type 2 (indices_wrong: {indices_wrong})')
                return False

    # check that all characters from p[i+1] are in word on other places than those covered by th
    represented_chars = set([c for c in ''.join(p[1:]) if c in ALPHABET_FULL])
    remaining_chars = set([c for c,rc in zip(word, right_chars) if c != rc])
    if not represented_chars.issubset(remaining_chars):
        # print(f'false type 3 (rep_chars:{"".join(represented_chars)} is not subset of rem_chars:{"".join(remaining_chars)})')
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
def main(guessed_word, char_combinations):
    """
    guessed_word - five char string consisting of ALPHABET_FULL or other
    characters such as '-'. Characters represent known 
    char_combination - list of five non-empty character sets consisting of ALPHABET or
    other character such as '-'. X in char_combination[i] means that the
    hidden word must contain X, but not on position i.
    Example: guessed_word = 'sp---' and char_combinations = ['-','-','-','i','c']
    means that the hidden word starts with sp and contains i and c whereas 
    must not be on 4-th position and c must not be on 5-th"""

    pattern = guessed_word + ' ' + ' '.join(char_combinations)

    char_freq = [Counter(), Counter(), Counter(), Counter(), Counter()]
    # a list of five counters; each counter counts occurences of a given 
    # character at the particular place; only characters from ALPHABET are used

    # calculate character frequencies
    words = load_words()
    valid_words = []
    for w in words:
        if valid(w, pattern):
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
    for(w,score) in matching_words.most_common(30):
        print(f'{w}, freq:{get_char_scores(w, char_freq)}')




###########################################################
def test_valid():

    t = [('hrnec', '----- - - - - -', True), ('hrnec', 'b---- - - - - -', False), ('hrnec', '-rn-- efg - - - -', False), 
         ('hrnec', 'h---- - - - - -', True), ('hrnec', 'h---- nec - - - -', True), ('hrnec', 'h---- - nec - - -', True),
         ('padák', 'p--a- - - a - -', True), ('pedál', 'p--a- - - a - -', False)] 

    for (word, pattern, expected) in t:
        res = valid(word, pattern)
        if expected == res:
            print(f'word:{word}, pattern:{pattern}, res:{res}')
        else:
            print(f'[TEST FAILED] word:{word}, pattern:{pattern}, res:{res}')
        print()



###########################################################
main('-----',['-','a','-','e','-'])

