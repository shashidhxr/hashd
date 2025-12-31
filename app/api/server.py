from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from app.core.db import get_connection
import os

from app.core.hash import sha256_file

app = Flask(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_DIR = os.path.join(BASE_DIR, "../../data/uploads")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/api_health")
def api_health():
    return {
        "status": "ok"
    }

@app.route("/db_health")
def db_health():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    cur.close()
    conn.close()
    return {
        "db": "ok"
    }

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({
            "error": "file not found",
        }), 400

    if file.filename == "":
        return jsonify({
            "error": "Empty filename"
        }), 400
    
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)
    print(path)

    checksum = sha256_file(path)

    return jsonify({
        "message": "file uploaded succesfully",
        "file": file.filename,
        "path": path,
        "checksum": checksum
    }), 200

if __name__ == "__main__":
    app.run(debug=True)