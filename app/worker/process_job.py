from app.core.db import sessionLocal
from app.models.job import Job
from app.models.file import File
from app.models.schema import Schema
from app.core.hash import sha256_file

import json
from jsonschema import validate, ValidationError

def process_job(job):
    session = sessionLocal()

    try:
        db_job = session.query(Job).filter_by(id=job.id).one()      # redundant? same as job passed(need when db is removed fo job discovery?)
        db_file = session.query(File).filter_by(id=job.file_id).one()
        db_schema = session.query(Schema).filter_by(id=db_file.schema_id).one()

        schema = db_schema.schema_json  

        rows = []
        with open(db_file.storage_path) as f:
            for line in f:
                rows.append(json.loads(line))   # NDJSON, need better way

        valid_rows = []
        invalid_rows = []

        for row in rows:
            try:
                validate(instance=row, schema=schema)
                valid_rows.append(row)
            except ValidationError as e:
                invalid_rows.append({"row": row, "error": str(e)})

        # Save results to Postgres or DLQ table later
        print("valid:", len(valid_rows))
        print("invalid:", len(invalid_rows))

        db_job.status = "SUCCESS"
        session.commit()

    except Exception:
        session.rollback()
        db_job.status = "FAILED"
        raise Exception
    finally:
        session.close()