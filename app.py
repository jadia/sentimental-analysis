from flask import Flask, render_template, flash, redirect, flash, url_for, session, logging, request, jsonify, make_response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from gettweets import AutomateAll, API

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
fileName = "UnstructTweets.json"


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchBar(request.form)

    if request.method == 'POST' and form.validate():
        keyword = request.form['keyword']
        #flash('Requested keywords: {}'.format(keyword))
        keywordAsList = Keyword2List(keyword)
        #analysis = TweepyUnitTest(keywordAsList.keyword2List())
        analysis = AutomateAll(keywordAsList.keyword2List())
        return render_template('result.html', keyword=keywordAsList, result=analysis.extractStructTweets())
    else:
        # keyword = request.form['keyword']
        # if len(keyword) == 0:
        #     invalid = 'Please provide input greater than '
        #     return render_template('home.html', form=form, invalid=invalid)
        return render_template('home.html', form=form)


@app.route('/api/<keyword>', methods=['GET'])
def get_tasks(keyword):
    keywordToList = Keyword2ListAPI(keyword)
    apiCall = API(keywordToList.keyword2List())
    apiReturn = apiCall.jsonAnalysis()
    if len(apiReturn) == 1:
        return jsonify(apiReturn), 200
    else:
        return make_response(jsonify({'error': 'Request not successful'}), 400)

    # return '%s' % apiReturn

# @app.route('/<wrongAddr>')
# def show404(wrongAddr):
#     return render_template('404.html')
#     # return 'Keywords are: %s' % keyword


class SearchBar(Form):
    keyword = StringField('Keyword', [validators.Length(min=2, max=50)])


class Keyword2List():
    def __init__(self, keyword):
        self.keyword = keyword

    def keyword2List(self):
        return(self.keyword.split(','))


class Keyword2ListAPI():
    def __init__(self, keyword):
        self.keyword = keyword

    def keyword2List(self):
        self.keyword.replace("%20", " ")
        return(self.keyword.split(','))


if __name__ == "__main__":
    app.run(debug=True)
