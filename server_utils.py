from flask import Flask, request
from flask_cors import CORS
import json
import sbd_utils


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(__name__)

    @app.route('/sentences', methods=['POST'])
    def get_sentences():
        text = request.form['text']
        return json.dumps(sbd_utils.text2sentences(text))

    @app.route('/offsets', methods=['POST'])
    def get_offsets():
        text = request.form['text']
        return json.dumps(sbd_utils.text2sentences(text, offsets=True))

    # --- DEV ROUTES --- #
    @app.route('/dev', methods=['GET'])
    def get_simple_msg():
        return json.dumps([{'text': 'dummy text ...', 'partType': 'header'},
                           {'text': 'dummy text ...', 'partType': 'proceedings'},
                           {'text': 'dummy text ...', 'partType': 'response'},
                           {'text': 'dummy text ...', 'partType': 'argumentation'},
                           {'text': 'dummy text ...', 'partType': 'footer'},
                           {'text': 'dummy text ...', 'partType': 'blah'}])

    @app.route('/deva', methods=['POST'])
    def print_post():
        json_body = request.get_json()
        return json.dumps([{'text': json_body['text'], 'partType': 'argumentation'}])

    return app
