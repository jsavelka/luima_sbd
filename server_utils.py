from flask import Flask, request
import json
import sbd_utils


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    @app.route('/segment', methods=['POST'])
    def segment_file():
        text = request.form['text']
        return json.dumps(sbd_utils.text2sentences(text))

    return app
