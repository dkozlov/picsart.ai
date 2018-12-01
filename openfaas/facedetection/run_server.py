from flask import Flask, request, jsonify
from handler import handle
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    return handle(request.get_data())

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=False)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
