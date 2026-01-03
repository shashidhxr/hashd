from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

import os

from app.core.hash import sha256_file
from app.core.db import sessionLocal
from app.models.file import File

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
    session = sessionLocal()

    try:
        session.execute(text("SELECT 1;"))
        return {
            "status": "ok"
        }, 200
    finally:
        session.close()

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

    session = sessionLocal()

    try:
        file_record = File(
            checksum = checksum,
            filename = filename,
            size_bytes = os.path.getsize(path),
            storage_path = path,
        )
        session.add(file_record)
        session.commit()

        return {
            "id": str(file_record.id),
            "checksum": checksum,
            "status": "stored",
        }, 201

    except IntegrityError:
        session.rollback()
        existing = session.query(File).filter_by(checksum=checksum).one()

        return {
            "id": str(existing.id),
            "checksum": checksum,
            "status": "duplicate"
        }, 200
    
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)