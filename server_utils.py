from flask import Flask, request
import json
import sbd_utils


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    @app.route('/sentences', methods=['POST'])
    def get_sentences():
        text = request.form['text']
        return json.dumps(sbd_utils.text2sentences(text))

    @app.route('/offsets', methods=['POST'])
    def get_offsets():
        text = request.form['text']
        return json.dumps(sbd_utils.text2sentences(text, offsets=True))

    return app
