import os
import requests
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="http://7b1fb1598c3c41a7b81577c1dee3488d@172.31.1.15:9000/2",
    debug=True,
    integrations=[FlaskIntegration()]
)

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

app = Flask(__name__)

Message = namedtuple('Message', 'text from_lang output_text')
messages = []


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    try:
        text = request.form['text']
        from_lang = request.form['from_lang']
        to_lang = 'ru'

        params = {
            'key': API_KEY,
            'text': text,
            'lang': '{}-{}'.format(from_lang, to_lang),
        }

        response = requests.get(URL, params=params)
        json_ = response.json()
        output_text = ''.join(json_['text'])
        messages.append(Message(text, from_lang, output_text))
        return redirect(url_for('main'))
    except Exception as error:
        sentry_sdk.capture_exception(error=error)
        return redirect(url_for('error'))


@app.route('/api/python')
def greeting():
    return 'Welcome, Python with Serverless!'


@app.route('/test-sentry')
def trigger_error():
    try:
        division_by_zero = 1 / 0
    except Exception as error:
        sentry_sdk.capture_exception(error=error)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
