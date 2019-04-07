from flask import Flask, Response, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    # data = request.data
    # data = data.json()
    # print(data)
    # response = request.get("http://localhost:5000")
    # print(response)
    return "Hi"

if __name__ == "__main__":
    app.run()