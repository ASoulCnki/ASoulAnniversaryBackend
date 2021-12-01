from flask import Flask, jsonify

from clickhouse import get_personal_data
from oauth import verify

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

@app.route('/AsoulAnniversary/<token>', methods=["GET"])
def asoul_anniversary(token):
    info = verify(token)
    if info!=None:
        return jsonify(wrap_response(get_personal_data(info.get("uid")))), 200
    else:
        return jsonify(wrap_response(None, code=404, message="授权状态错误")), 200

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)