from flask import Flask, render_template, flash, redirect, flash, url_for, session, logging, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from unitTest import TweepyUnitTest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
fileName = "UnstructTweets.json"


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchBar(request.form)

    if request.method == 'POST':
        keyword = request.form['keyword']
        #flash('Requested keywords: {}'.format(keyword))
        keywordAsList = Keyword2List(keyword)
        analysis = TweepyUnitTest(keywordAsList.keyword2List())
        return render_template('result.html', keyword=keywordAsList, result=analysis.analyse())
    else:
        #flash('Things not working out')
        return render_template('home.html', form=form)


@app.route('/<keyword>')
def getTweets(keyword):
    return 'Keywords are: %s' % keyword


class SearchBar(Form):
    keyword = StringField('Keyword', [validators.Length(min=1, max=50)])


class Keyword2List():
    def __init__(self, keyword):
        self.keyword = keyword

    def keyword2List(self):
        return(self.keyword.split(','))


if __name__ == "__main__":
    app.run(debug=True)
