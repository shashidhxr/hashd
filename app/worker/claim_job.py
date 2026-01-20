from app.core.db import sessionLocal
from app.models.job import Job

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
