# seed.py — Populate database with fake data using Faker
# Creates groups, teachers, subjects, students, and grades

import random
from datetime import datetime, timedelta, timezone
from faker import Faker
import os
from models import (
    Base,
    get_engine,
    get_session,
    Group,
    Student,
    Teacher,
    Subject,
    Grade,
)

fake = Faker()
engine = get_engine(os.getenv("DATABASE_URL"))
Session = get_session(engine)


# -----------------------------
# Drop and recreate all tables
# -----------------------------
def recreate_schema():
    """Drop all tables and recreate schema."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# -----------------------------
# Seed database
# -----------------------------
def seed(
    n_students=40, n_groups=3, n_teachers=5, n_subjects=7, max_grades_per_student=20
):
    """Populate database with fake data."""
    session = Session()
    try:
        # Create groups
        groups = [Group(name=f"Group-{i+1}") for i in range(n_groups)]
        session.add_all(groups)
        session.flush()

        # Create teachers
        teachers = [
            Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
            )
            for _ in range(n_teachers)
        ]
        session.add_all(teachers)
        session.flush()

        # Subject names
        subject_names = [
            "Math",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "English",
            "Art",
        ]

        # Create subjects with random teachers
        subjects = [
            Subject(
                name=subject_names[i % len(subject_names)],
                teacher=random.choice(teachers),
            )
            for i in range(n_subjects)
        ]
        session.add_all(subjects)
        session.flush()

        # Create students assigned to random groups
        students = [
            Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                group=random.choice(groups),
            )
            for _ in range(n_students)
        ]
        session.add_all(students)
        session.flush()

        # Create grades for students
        for student in students:
            for _ in range(random.randint(5, max_grades_per_student)):
                subj = random.choice(subjects)
                grade_value = round(random.uniform(2.0, 5.0), 2)
                created_at = datetime.now(timezone.utc) - timedelta(
                    days=random.randint(0, 365)
                )
                session.add(
                    Grade(
                        student=student,
                        subject=subj,
                        grade=grade_value,
                        created_at=created_at,
                    )
                )

        session.commit()
        print("\033[92mSeeding finished.\033[0m.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# -----------------------------
# Run seeding if executed directly
# -----------------------------
if __name__ == "__main__":
    recreate_schema()
    seed()
