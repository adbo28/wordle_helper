

from collections import Counter



ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_FULL =     'aábcčdďeěéfghiíjklmnňoópqrřsštťuůúvwxyýzž'
ALPHABET_MAPPING =  'aabccddeeefghiijklmnnoopqrrssttuuuvwxyyzz'

FILENAME = 'slovnik5.txt'


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
    indices_wrong = [i for i in range(5) if pattern[i] in ALPHABET_FULL and pattern[i] != word[i]]
    if len(indices_wrong):
        if report_errors:
            print(f'false type 1 (indices_wrong: {indices_wrong})')
        return False

    # check that word does not contain char from p[i+1] on place i
    for i in range(5):
        if pattern[i] not in ALPHABET_FULL:
            # only checked if p[i+1] is relevant, i.e. if the character on the given place is not known yet
            w = misplaced_chars[i]
            indices_wrong = [c for c in w if word2[i] == c]
            if len(indices_wrong):
                if report_errors:
                    print(f'false type 2 (indices_wrong: {indices_wrong})')
                return False

    # check that all characters from p[i+1] are in word on other places than those covered by th
    represented_chars = set([c for c in ''.join(misplaced_chars) if c in ALPHABET_FULL])
    remaining_chars = set([c for c,rc in zip(word2, pattern) if c != rc])
    if not represented_chars.issubset(remaining_chars):
        if report_errors:
            print(f'false type 3 (rep_chars:{"".join(represented_chars)} is not subset of rem_chars:{"".join(remaining_chars)})')
        return False

    # check that the word does not contain forbidden characters
    word_chars = set(word2)
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
    """Calculates score for a given word a sum of squares of the score
    of each characted."""
    return sum([x**2 for x in get_char_scores(word, char_freq)])


###########################################################
def update_freq(word, char_freq):
    """char_freq is a list of five Counters that maintain information
    about the frequencies of particular characters at the given position.
    This function updates the frequencies based on the given word."""
    word2 = replace_special_chars(word)
    for c, cntr in zip(word2, char_freq):
        cntr[c] += 1

