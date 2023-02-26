# -*- coding: utf-8 -*-

from dotenv import load_dotenv

load_dotenv(verbose=True)
from common_sdk.util.monkey_json import monkey_patch_json, UJSONEncoder

monkey_patch_json()

from flask import Flask
from service.init_blueprint import init_blueprint

app = Flask("chatgpt_service")
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=False, JSON_SORT_KEYS=False, JSON_AS_ASCII=False, DEBUG=False)
app.json_encoder = UJSONEncoder
init_blueprint(app)

if __name__ == '__main__':
    app.run()
