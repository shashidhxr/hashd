from app.core.db import sessionLocal
from app.models.job import Job
from app.models.file import File
from app.core.hash import sha256_file

from time import time

def claim_job():
    session = sessionLocal()

    try:
        job = (
            session.query(Job).filter(Job.status == "PENDING")
                .with_for_update(skip_locked=True)
                .first()
        )
        if job is None:
            session.close()
            return None
        
        job.status = "RUNNING"
        session.commit()

        return job
    except Exception:
        session.rollback()
        raise Exception
    finally:
        session.close()

def process_job():
    session = sessionLocal()

    try:
        db_job = session.query(Job).filter_by(id=Job.id).one()
        db_file = session.query(File).filter_by(id=Job.file_id).one()

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

def worker_loop():
    print("worker started")

    while True:
        job = claim_job()

        if not job:
            time.sleep(2)
            continue
    
        print(f"[worker] claimed job {job.id}, processing")

        try:
            process_job(job)
            print(f"[worker] Job {job.id} completed.")
        except Exception as e:
            print(f"[worker] Job {job.id} failed: {e}")

if __name__ == "__main__":
    worker_loop()