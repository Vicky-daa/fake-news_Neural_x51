from flask import Flask, render_template, url_for, request
import joblib
import re
import string
import pandas as pd

application = Flask(__name__)
app = application
Model = joblib.load("model.pkl")


# @app.route('/')
# def index():
#     return render_template("index.html")


def wordpre(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)  # remove special chars
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text


@app.route('/', methods=['GET','POST'])
def pre():
    if request.method == 'GET':
        result='_'
        return render_template("index.html", result=result)

    if request.method == 'POST':
        txt = request.form['txt']
        txt = wordpre(txt)
        txt = pd.Series(txt)
        result = Model.predict(txt)
        return render_template("index.html", result=result)
    return ''


if __name__ == "__main__":
    app.run(debug=True)
