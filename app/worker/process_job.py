from app.core.db import sessionLocal
from app.models.job import Job
from app.models.file import File
from app.core.hash import sha256_file

def process_job(job):
    session = sessionLocal()

    try:
        db_job = session.query(Job).filter_by(id=job.id).one()
        db_file = session.query(File).filter_by(id=job.file_id).one()

        new_checksum = sha256_file(db_file.storage_path)

        if new_checksum == db_file.checksum:
            db_job.status = "SUCCESS"
            db_job.error = None
        else:
            db_job.status = "FAILED"
            db_job.error = (
                f"Checksum mismatch: expected {db_file.checksum}, got {new_checksum}"
            )

        session.commit()

    except Exception:
        session.rollback()
        raise Exception
    finally:
        session.close()