
from collections import Counter

from flask import Flask, render_template, url_for, request, redirect

from util import load_words, valid, update_freq, calc_score, get_char_scores


app = Flask(__name__)



###########################################################
def analyze_words(pattern, misplaced_chars, forbidden_chars):

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
    res = ''
    res += f'<h3>valid words: {len(matching_words)}</h3>'
    res += f'<h3>best word: {best_word}</h3>'

    res += '<h3>next words:</h3><p>'
    for(w,score) in matching_words.most_common(min(len(matching_words), 30)):
        res += f'{w}, freq:{get_char_scores(w, char_freq)}<br>'
    res += '</p>'

    res += '<h3>character frequency:</h3><p>'
    for i, cntr in enumerate(char_freq):
        res += f'position {(i+1)}: {cntr.most_common(5)}<br>'
    res += '</p>'

    return res



###########################################################
@app.route("/", methods = ['GET', 'POST'])
def main():

    main_pattern = ''
    mis_chars1 = ''
    mis_chars2 = ''
    mis_chars3 = ''
    mis_chars4 = ''
    mis_chars5 = ''
    forbidden_chars = ''
    res = ''


    if request.method == 'POST':
        main_pattern = (request.values.get('main_pattern') + '-----')[0:5]
        mis_chars1 = request.values.get('mis_chars1')
        mis_chars2 = request.values.get('mis_chars2')
        mis_chars3 = request.values.get('mis_chars3')
        mis_chars4 = request.values.get('mis_chars4')
        mis_chars5 = request.values.get('mis_chars5')
        forbidden_chars = request.values.get('forbidden_chars')

        res = analyze_words(main_pattern, [mis_chars1, mis_chars2, mis_chars3, mis_chars4, mis_chars5], forbidden_chars)



    return render_template(
        'index.html',
        main_pattern = main_pattern,
        mis_chars1 = mis_chars1, 
        mis_chars2 = mis_chars2, 
        mis_chars3 = mis_chars3, 
        mis_chars4 = mis_chars4, 
        mis_chars5 = mis_chars5, 
        forbidden_chars = forbidden_chars,
        res = res
    )
