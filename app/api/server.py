from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from uuid import UUID

import os

from app.core.hash import sha256_file
from app.core.db import sessionLocal
from app.models.file import File
from app.models.job import Job

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
    # print(path)

    checksum = sha256_file(path)
    size_bytes = os.path.getsize(path)

    session = sessionLocal()

    try:
        file_record = File(
            checksum = checksum,
            filename = filename,
            size_bytes = size_bytes,
            storage_path = path,
        )
        session.add(file_record)

        session.flush()

        job = Job(
            file_id = file_record.id,
            type = "VERIFY_INTEGRITY",
            status = "PENDING",
        )
        
        session.add(job)
        session.commit()

        return {
            "file_id": str(file_record.id),
            "job_id": str(job.id),
            "status": "PENDING",
        }, 202

    except IntegrityError:
        session.rollback()

        existing_file = session.query(File).filter_by(checksum=checksum).one()

        job = Job(
            file_id=existing_file.id,
            type="VERIFY_INTEGRITY",
            status="PENDING",
        )
        session.add(job)
        session.commit()

        return {
            "file_id": str(existing_file.id),
            "job_id": str(job.id),
            "status": "PENDING",        # not true status
            "message": "duplicate file"
        }, 202
    
    finally:
        session.close()

@app.route("/jobs")
def get_jobs():
    session = sessionLocal()

    try:
        jobs = session.query(Job).all()
        return {
            "jobs": [
                {
                    "id": str(job.id),
                    "file_id": str(job.file_id),
                    "type": job.type,
                    "status": job.status,
                    "error": job.error,
                    "created_at": job.created_at.isoformat(),
                    "updated_at": job.updated_at.isoformat(),
                }
                for job in jobs
            ]
        }, 200
    finally:
        session.close()

@app.route("/jobs/<job_id>")
def get_job(job_id):
    session = sessionLocal()

    # fails for wrong invalid uuid
    job = session.query(Job).filter(Job.id == UUID(job_id)).one_or_none()

    try:
        if job is None:
            return {
                "error": "job not found"
            }, 404
        
        return {
            "id": str(job.id),
            "file_id": str(job.file_id),
            "type": job.type,
            "status": job.status,
            "error": job.error,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
        }, 200
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)