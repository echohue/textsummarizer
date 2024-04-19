from flask import Flask,render_template,request
from app import extractsummarizer,abstractsummarizer

menu = Flask(__name__)
@menu.route('/')
def index():
    return render_template('index.html')
@menu.route('/analyze', methods = ['GET', 'POST'])


def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary,text,len_txt,len_summ = extractsummarizer(rawtext)
    return render_template('summary.html',summary = summary, text=text, len_txt=len_txt,len_summ=len_summ)

@menu.route('/analyze1', methods = ['GET', 'POST'])

def analyze1():
    if request.method == 'POST':
        rawtext = request.form['rawtext1']
        summary,text = abstractsummarizer(rawtext)
    return render_template('asummary.html',summary = summary,text = text)


if __name__ =="__main__":
    menu.run(debug = True)