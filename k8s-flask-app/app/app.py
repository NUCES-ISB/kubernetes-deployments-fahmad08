from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection details from environment variables
DB_NAME = os.getenv("POSTGRES_DB", "flaskdb")
DB_USER = os.getenv("POSTGRES_USER", "flaskuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# API to test database connection
@app.route("/")
def index():
    return "Flask App with PostgreSQL is Running!"

# API to create a table
@app.route("/init", methods=["GET"])
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    return "Table Created!", 200

# API to insert a user
@app.route("/add", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s) RETURNING id", (name,))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"id": user_id, "name": name}), 201

# API to retrieve all users
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify([{"id": u[0], "name": u[1]} for u in users]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
