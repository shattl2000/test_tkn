import os
import requests
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

app = Flask(__name__)

Message = namedtuple('Message', 'text tag output_text')
messages = []


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    from_lang = tag
    to_lang = 'ru'

    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    output_text = ''.join(json_['text'])
    messages.append(Message(text, tag, output_text))
    return redirect(url_for('main'))


@app.route('/api/python')
def greeting():
    return 'Welcome, Python with Serverless!'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
