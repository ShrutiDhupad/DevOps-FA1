from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Backend API is running",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    })

@app.route("/api/hello")
def hello():
    return jsonify({
        "message": "Hello from the DevOps Backend!",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)