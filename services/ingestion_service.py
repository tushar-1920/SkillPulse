# ingestion_service.py
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import pandas as pd
from pathlib import Path

from database.db import SessionLocal, engine, Base
from database.models import JobPosting, JobSkill


def ingest_all():

    Base.metadata.create_all(bind=engine)

    base_dir = Path(__file__).resolve().parent.parent

    jobs_path = base_dir / "data" / "processed_jobs.csv"
    skills_path = base_dir / "data" / "normalized_skills.csv"

    jobs_df = pd.read_csv(jobs_path)
    skills_df = pd.read_csv(skills_path)

    session = SessionLocal()

    print("Inserting jobs...")

    job_id_map = {}

    for idx, row in jobs_df.iterrows():

        job = JobPosting(
            title=row.get("title", ""),
            company=row.get("company", ""),
            location=row.get("location", ""),
            description=row.get("cleaned_description", "")
        )

        session.add(job)
        session.flush()          # get generated id

        job_id_map[idx] = job.id

    print("Inserting skills...")

    for _, row in skills_df.iterrows():

        original_job_id = int(row["job_id"])

        if original_job_id not in job_id_map:
            continue

        js = JobSkill(
            job_id=job_id_map[original_job_id],
            skill=row["normalized_skill"]
        )

        session.add(js)

    session.commit()
    session.close()

    print("Data successfully stored in SQLite.")


if __name__ == "__main__":
    ingest_all()
