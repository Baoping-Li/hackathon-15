"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request
from flask import jsonify

import capital
import utility


app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'



@app.route('/api/status', methods=['GET' ])
def capital_status():
    status = {}
    status['insert'] = True
    status['fetch'] = True
    status['delete'] = True
    status['list'] = True
    return json.dumps(status)

@app.route('/api/capitals/<id>', methods=['DELETE', 'PUT', 'GET' ])
def capital_operations(id):
    """handle capitals requests"""

    data = {}
    try:
      if request.method == 'PUT':
        print json.dumps(request.get_json())

        a_capital = capital.Capital()

        print json.dumps(request.get_json()['id'])
        a_capital.store(request.get_json(), id)

        return '', 200
        
      elif request.method == 'DELETE':
        a_capital = capital.Capital()
        a_capital.delete(id)

        return '', 200

      elif request.method == "GET":    

        a_capital = capital.Capital()
        json_capital = a_capital.get(id)
        
        if not json_capital:
          return '{ "code": 404, "message": "Capital not found" }', 404
        return jsonify(json_capital), 200
        #return json.dumps(json_capital), 200

    except Exception as e:
        # swallow up exceptions
        logging.exception('Oops!')

    return "Unexpected error", 500


@app.route('/api/capitals', methods=['GET'])
def list_capitals():
    """list capitals"""

    a_capital = capital.Capital()
    results = a_capital.fetch()
    return jsonify(results)

@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
