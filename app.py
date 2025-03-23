import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

# Correct template path
app = Flask(__name__, template_folder="templates")

# Connect to MongoDB
client = MongoClient("mongodb+srv://krishnabk0803:keshika0803@cluster0.5jw6k.mongodb.net/database")
db = client["database"]
collection = db["collection"]

@app.route("/")
def home():
    return render_template("index.html")  # Serve index.html

@app.route("/search", methods=["GET"])
def search_buses():
    start = request.args.get("start")
    end = request.args.get("end")

    if not start or not end:
        return jsonify({"error": "Please provide both start and end locations"}), 400

    buses = collection.find({"start": start, "end": end}, {"busName": 1, "time": 1, "_id": 0})
    
    result = list(buses)  # Convert cursor to list

    if not result:
        return jsonify({"message": "No matching buses found."})

    return jsonify(result)  # Returns only busName and time

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
