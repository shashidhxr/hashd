from app.worker.claim_job import claim_job
from app.worker.process_job import process_job

import time

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