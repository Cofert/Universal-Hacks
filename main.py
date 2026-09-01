from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/api/input', methods=['POST', 'OPTIONS'])
def receive_input():
    if request.method == 'OPTIONS':
        return _cors('', 204)
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()
    if not text:
        return _cors(jsonify({'error': 'No text provided'}), 400)
    logger.info('INPUT: %s', text)
    return _cors(jsonify({'ok': True, 'received': text}), 200)

def _cors(body, status):
    if isinstance(body, str):
        from flask import Response
        resp = Response(body, status=status)
    else:
        resp = app.make_response((body, status))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
