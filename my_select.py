# SQLAlchemy queries for students, teachers, subjects, and grades.
# Uses session from models.py, no external connect.py required.
# Outputs in tables using tabulate.

from sqlalchemy import func, desc
from tabulate import tabulate
from models import get_engine, get_session
from models import Student, Group, Subject, Teacher, Grade

# Initialize SQLAlchemy session factory
Session = get_session(get_engine())


# Helper to format average grades
def format_avg(avg):
    return float(f"{avg:.2f}") if avg is not None else None


# -----------------------------
# 1. Top 5 students by average grade
# -----------------------------
def select_1():
    with Session() as session:
        rows = (
            session.query(
                func.concat(Student.first_name, " ", Student.last_name).label("name"),
                func.avg(Grade.grade).label("avg_grade"),
            )
            .join(Grade)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
            .all()
        )
        table = [[r.name, format_avg(r.avg_grade)] for r in rows]
        print(tabulate(table, headers=["Student", "Average Grade"], tablefmt="psql"))
        return table


# -----------------------------
# 2. Student with highest average in a subject
# -----------------------------
def select_2(subject_name: str):
    with Session() as session:
        r = (
            session.query(
                func.concat(Student.first_name, " ", Student.last_name).label("name"),
                func.avg(Grade.grade).label("avg_grade"),
            )
            .join(Grade)
            .join(Subject)
            .filter(Subject.name == subject_name)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .first()
        )
        if r:
            table = [[r.name, format_avg(r.avg_grade)]]
            print(
                tabulate(table, headers=["Student", "Average Grade"], tablefmt="psql")
            )
            return table
        return []


# -----------------------------
# 3. Average grade per group for a subject
# -----------------------------
def select_3(subject_name: str):
    with Session() as session:
        rows = (
            session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject)
            .filter(Subject.name == subject_name)
            .group_by(Group.id)
            .all()
        )
        table = [[r.name, format_avg(r.avg_grade)] for r in rows]
        print(tabulate(table, headers=["Group", "Average Grade"], tablefmt="psql"))
        return table


# -----------------------------
# 4. Overall average grade
# -----------------------------
def select_4():
    with Session() as session:
        avg = session.query(func.avg(Grade.grade)).scalar()
        avg_formatted = format_avg(avg)
        print(tabulate([[avg_formatted]], headers=["Overall Average"], tablefmt="psql"))
        return avg_formatted


# -----------------------------
# 5. Courses taught by a teacher
# -----------------------------
def select_5(teacher_id: int):
    with Session() as session:
        rows = (
            session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        )
        table = [[r.name] for r in rows]
        print(tabulate(table, headers=["Course"], tablefmt="psql"))
        return [r[0] for r in rows]


# -----------------------------
# 6. Students in a specific group
# -----------------------------
def select_6(group_id: int):
    with Session() as session:
        rows = (
            session.query(
                func.concat(Student.first_name, " ", Student.last_name).label("name")
            )
            .filter(Student.group_id == group_id)
            .all()
        )
        table = [[r.name] for r in rows]
        print(tabulate(table, headers=["Student"], tablefmt="psql"))
        return [r[0] for r in rows]


# -----------------------------
# 7. Grades for a group in a specific subject
# -----------------------------
def select_7(group_id: int, subject_name: str):
    with Session() as session:
        rows = (
            session.query(
                func.concat(Student.first_name, " ", Student.last_name).label("name"),
                Grade.grade,
                Grade.created_at,
            )
            .join(Grade)
            .join(Subject)
            .filter(Student.group_id == group_id, Subject.name == subject_name)
            .order_by("name", Grade.created_at)
            .all()
        )
        table = [[r.name, r.grade, str(r.created_at)] for r in rows]
        print(tabulate(table, headers=["Student", "Grade", "Date"], tablefmt="psql"))
        return table


# -----------------------------
# 8. Average grade given by a teacher
# -----------------------------
def select_8(teacher_id: int):
    with Session() as session:
        avg = (
            session.query(func.avg(Grade.grade))
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.teacher_id == teacher_id)
            .scalar()
        )
        avg_formatted = format_avg(avg)
        print(tabulate([[avg_formatted]], headers=["Average Grade"], tablefmt="psql"))
        return avg_formatted


# -----------------------------
# 9. Courses a student attends
# -----------------------------
def select_9(student_id: int):
    with Session() as session:
        rows = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id)
            .distinct()
            .all()
        )
        table = [[r.name] for r in rows]
        print(tabulate(table, headers=["Course"], tablefmt="psql"))
        return [r[0] for r in rows]


# -----------------------------
# 10. Courses a student attends with a specific teacher
# -----------------------------
def select_10(student_id: int, teacher_id: int):
    with Session() as session:
        rows = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .distinct()
            .all()
        )
        table = [[r.name] for r in rows]
        print(tabulate(table, headers=["Course"], tablefmt="psql"))
        return [r[0] for r in rows]


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":

    subjectName = "Biology"

    print("\n\033[93m 1. Top 5 students:\033[0m.")
    select_1()

    subjectName = "Biology"
    print(f"\n\033[93m 2. Best student in {subjectName}:\033[0m.")
    select_2(subjectName)

    print(f"\n\033[93m 3. Average grade per group in {subjectName}:\033[0m.")
    select_3(subjectName)

    print("\n\033[93m 4. Overall average grade:\033[0m.")
    select_4()

    print("\n\033[93m 5. Courses by teacher 1:\033[0m.")
    select_5(1)

    print("\n\033[93m 6. Students in group 1:\033[0m.")
    select_6(1)

    print(f"\n\033[93m 7. Grades for group 1 in {subjectName}:\033[0m.")
    select_7(1, subjectName)

    print("\n\033[93m 8. Average grade by teacher 1:\033[0m.")
    select_8(1)

    print("\n\033[93m 9. Courses attended by student 1:\033[0m.")
    select_9(1)

    print("\n\033[93m 10. Courses student 1 attends with teacher 1:\033[0m.")
    select_10(1, 1)
