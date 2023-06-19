from flask import Flask, render_template, request, redirect, jsonify, url_for
from model import parameters_get

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api():
    start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')
    # symbol = request.args.get('symbol')

    response = parameters_get().get(start=start_date)
    return response

    # start_date = request.args.get('start_date', 'No input')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=5000)