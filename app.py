from flask import Flask, render_template, request, url_for, redirect, flash
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import RegexpTokenizer
from fastapi import FastAPI
nltk.download('vader_lexicon')

app = Flask(__name__)
app.secret_key = "super secret key"
@app.route('/', methods=['POST', 'GET'])
def index():
    results = []
    score_dict = {}
    text = ""
    if request.method == 'POST':    
        text = request.form['data']
        if text == "":
            flash("Please enter some text first")
        else:
            results, score_dict = sentiment_scores(text)
    
    labels = [key for key in score_dict]
    values = [score_dict[key] for key in score_dict]
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    if labels:
        labels.pop()
        values.pop()
    return render_template('index.html', results=results, score_dict=score_dict,
                labels=labels, values=values, tokens=tokens)


def sentiment_scores(data):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(data)
    list1 = []
    list1.append("Your text is, ")
    list1.append("{:.3f} % Negative".format(sentiment_dict['neg']*100))
    list1.append("{:.3f} % Neutral".format(sentiment_dict['neu']*100))
    list1.append("{:.3f} % Positive".format(sentiment_dict['pos']*100))
    return list1, sentiment_dict 


if __name__ == "__main__":
    app.run(debug=True)
           
