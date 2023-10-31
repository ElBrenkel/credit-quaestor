from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/getexample", methods=["GET"])
def get_data():
    data = {"message": "This is data from the API"}
    return jsonify(data)


@app.route("/parameterexample", methods=["GET"])
def get_parameter():
    code = request.args.get("code")
    if code is None:
        print("bad" + code)
        return jsonify({"error": "Missing 'username' query parameter"}), 400
    print("good" + code)
    return jsonify({"code": code})


@app.route("/postexample", methods=["POST"])
def send_data():
    data = request.get_json()
    return jsonify({"message": "Data received", "data": data})


if __name__ == "__main__":
    app.run()
