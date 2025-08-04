from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("Mongo_URL"))
db = client["UserData"]
users = db["users"]

CORS(app)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    print("Hiii")
    return "success", 200

@app.route('/data', methods=['GET', 'POST'])
def first():
    print("Hello")
    if request.method == 'GET':
        return jsonify({"message": "GET request received. Nothing to see here!"}), 200

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.json

    if "email" not in data:
        return jsonify({"error": "Missing 'email' in request"}), 400

    user = users.find_one({"email": data["email"]})
    if user:
        return jsonify({"message": "Message Already Sent"}), 400

    users.insert_one(data)
    return jsonify({"message": "Data inserted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True) 