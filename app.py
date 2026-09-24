from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["flask_database"]
students_collection = db["students"]


@app.route("/")
def home():
    return render_template("index.html")


# Task 1: data.json se data read karna
@app.route("/api")
def api_data():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "data.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)


# MongoDB connection test
@app.route("/mongo-test")
def mongo_test():
    try:
        client.admin.command("ping")

        return jsonify({
            "status": "success",
            "message": "MongoDB connected successfully"
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


# Form data MongoDB mein save karna
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        course = request.form.get("course")

        if not name or not course:
            return render_template(
                "index.html",
                error="Please fill in all fields."
            )

        student_data = {
            "name": name,
            "course": course
        }

        students_collection.insert_one(student_data)

        return render_template("success.html")

    except Exception as error:
        return render_template(
            "index.html",
            error=f"Error: {error}"
        )

@app.route("/submittodoitem", methods=["POST"])
def submittodoitem():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    students_collection.insert_one(todo_item)

    return render_template("success.html")
if __name__ == "__main__":
    app.run(debug=True) 
    