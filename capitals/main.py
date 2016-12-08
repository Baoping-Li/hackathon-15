"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request, send_from_directory
from flask import jsonify

import capital
import utility


app = Flask(__name__)

@app.route('/')
def hello_world():
    """hello world"""
    return send_from_directory('', 'index.html')

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('', path)


@app.route('/api/status', methods=['GET' ])
def capital_status():
    status = {}
    status['insert'] = True
    status['fetch'] = True
    status['delete'] = True
    status['list'] = True
    status['query'] = True
    status['search'] = True
    status['pubsub'] = True
    status['storage'] = True
    return json.dumps(status)

@app.route('/api/capitals/<id>', methods=['DELETE', 'PUT', 'GET' ])
def capital_operations(id):
    """handle capitals requests"""

    data = {}
    try:
      if request.method == 'PUT':
        #print json.dumps(request.get_json())

        a_capital = capital.Capital()

        #print json.dumps(request.get_json()['id'])
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

    except Exception as e:
        # swallow up exceptions
        logging.exception('Oops!')

    return "Unexpected error", 500


@app.route('/api/capitals', methods=['GET'])
def list_capitals():
    """list capitals"""

    a_capital = capital.Capital()
    search = request.args.get('search')
    query = request.args.get('query')
    if search:
        results = a_capital.fetch()
        found = []
        for capital_data in results:
            if search in json.dumps(capital_data):
                found.append(capital_data)
        #if len(found) == 0:
            #return '{ "code": 404, "message": "Not found" }', 404
        return jsonify(found), 200
    elif query:
        query_items = query.split(':')
        results = a_capital.fetch(20, query_items[0], query_items[1])
        return jsonify(results), 200

    results = a_capital.fetch(20)
    return jsonify(results), 200

@app.route('/api/capitals/<id>/store', methods=['POST']) 
def store_capital(id):
    """store capitals"""

    #print json.dumps(request.get_json())
    bucket = request.get_json()['bucket']
    #print bucket
    if not bucket:
        return '{ "code": 500, "message": "Bad request" }', 500
    a_capital = capital.Capital()
    capital_data = a_capital.get(id)
    if not capital_data:
        return '{ "code": 404, "message": "Capital not found" }', 404
    #print capital_data
    a_capital.cloud_store(bucket, capital_data)
    return '', 200

@app.route('/api/capitals/<id>/publish', methods=['POST']) 
def publish_capital(id):
    """publish capitals"""
    try:
        topic = request.get_json()['topic']
        #print topic
        if not topic:
            return '{ "code": 500, "message": "Bad request" }', 500
        a_capital = capital.Capital()
        capital_data = a_capital.get(id)
        if not capital_data:
            return '{ "code": 404, "message": "Capital not found" }', 404
        #print capital_data
        message_id = a_capital.publish(topic, capital_data)
        response = {"messageId" : int(message_id)}
        return jsonify(response), 200
    except Exception as e:
        # swallow up exceptions
        logging.exception('Oops!')
        print e

    return "Unexpected error", 500

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
