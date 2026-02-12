# market_service.py
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from sqlalchemy import func
from database.db import SessionLocal
from database.models import JobSkill


def get_top_skills(limit=10):
    session = SessionLocal()

    rows = (
        session.query(
            JobSkill.skill,
            func.count(JobSkill.skill).label("cnt")
        )
        .group_by(JobSkill.skill)
        .order_by(func.count(JobSkill.skill).desc())
        .limit(limit)
        .all()
    )

    session.close()

    return [{"skill": r[0], "count": r[1]} for r in rows]
