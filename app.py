from flask import Flask, render_template, flash, redirect, flash, url_for, session, logging, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from unitTest import TweepyUnitTest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchBar(request.form)

    if request.method == 'POST':
        keyword = request.form['keyword']
        flash('Requested keywords: {}'.format(keyword))
        analysis = TweepyUnitTest(keyword)
        return render_template('result.html', keyword=keyword, result=analysis.analyse())
    else:
        #flash('Things not working out')
        return render_template('home.html', form=form)


@app.route('/<keyword>')
def getTweets(keyword):
    return 'Keywords are: %s' % keyword


class SearchBar(Form):
    keyword = StringField('Keyword', [validators.Length(min=1, max=50)])


if __name__ == "__main__":
    app.run(debug=True)
