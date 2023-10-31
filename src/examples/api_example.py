from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/getexample', methods=['GET'])
def get_data():
    data = {'message': 'This is data from the API'}
    return jsonify(data)


@app.route('/parameterexample', methods=['GET'])
def get_parameter():
    username = request.args.get('username')
    if username is None:
        return jsonify({"error": "Missing 'username' query parameter"}), 400
    return jsonify({"username": username})


@app.route('/postexample', methods=['POST'])
def send_data():
    data = request.get_json()
    return jsonify({'message': 'Data received', 'data': data})


if __name__ == '__main__':
    app.run()
