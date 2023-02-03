

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/", methods = ['GET', 'POST'])
def main():

    main_pattern = ''
    action = ''
    html = ''
    show_form = True

    if request.method == 'POST':
        main_pattern = request.values.get('main_pattern')




    return render_template(
        'index.html',
        main_pattern = main_pattern,
        mis_chars1 = '', 
        mis_chars2 = '', 
        mis_chars3 = '', 
        mis_chars4 = '', 
        mis_chars5 = '', 
        forbidden_chars = '',
        matched_count = 0,
        matched_words = ''
    )
