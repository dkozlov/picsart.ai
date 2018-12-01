from flask import Flask, request, jsonify
from handler import handle

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    return handle(request.get_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
