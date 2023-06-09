from flask import Flask, render_template, request, redirect, jsonify, url_for


app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def login():
    start_date = request.args.get('start_date', 'No input')
    end_date = request.args.get('end_date', 'No input')
    symbol = request.args.get('symbol', 'No input')
    # start_date = request.args.get('start_date', 'No input')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=5000)