from flask import Flask, jsonify

from mysql import get_personal_data

from config import FLASK_PORT, FLASK_HOST

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

def wrap_response(data, code=0, message=""):
    result = {
        "code": code,
        "message": message,
        "data": data
    }
    return result

@app.route('/AsoulAnniversary/<uid>', methods=["GET"])
def asoul_anniversary(uid):
    return jsonify(wrap_response(get_personal_data(uid))), 200

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)