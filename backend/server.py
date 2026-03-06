from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rishu0816",
    database="exam_ai"
)

cursor = db.cursor()

# Home Route
@app.route("/")
def home():
    return "AI Based Competitive Exam Preparation Assistant Backend Running"

# Register API
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    query = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
    cursor.execute(query, (name, email, password))
    db.commit()

    return jsonify({"message": "User registered successfully"})

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid email or password"})

@app.route("/questions", methods=["GET"])
def get_questions():
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    result = []
    for q in questions:
        result.append({
            "id": q[0],
            "question": q[1],
            "optionA": q[2],
            "optionB": q[3],
            "optionC": q[4],
            "optionD": q[5],
            "correct_answer": q[6],
            "category": q[7]
        })

    return jsonify(result)
@app.route("/submit-test", methods=["POST"])
def submit_test():
    data = request.json

    user_id = data["user_id"]
    score = data["score"]

    query = "INSERT INTO results (user_id, score) VALUES (%s,%s)"
    cursor.execute(query, (user_id, score))
    db.commit()

    return jsonify({"message": "Test result saved successfully"})
if __name__ == "__main__":
    app.run(debug=True)