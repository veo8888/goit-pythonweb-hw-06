# models.py — SQLAlchemy ORM models and session utilities
# Defines tables: Group, Student, Teacher, Subject, Grade
# Provides engine and session creation functions.

from datetime import datetime
import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# Base class for ORM models
Base = declarative_base()


# -----------------------------
# Group model
# -----------------------------
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    students = relationship("Student", back_populates="group")


# -----------------------------
# Student model
# -----------------------------
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    group = relationship("Group", back_populates="students")
    grades = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )


# -----------------------------
# Teacher model
# -----------------------------
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


# -----------------------------
# Subject model
# -----------------------------
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship(
        "Grade", back_populates="subject", cascade="all, delete-orphan"
    )


# -----------------------------
# Grade model
# -----------------------------
class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


# -----------------------------
# Utility: Get SQLAlchemy engine
# -----------------------------
def get_engine(url: str = None):
    """Create a SQLAlchemy engine."""
    if url is None:
        url = os.getenv("DATABASE_URL")
    return create_engine(url, echo=False, future=True)


# -----------------------------
# Utility: Get session factory
# -----------------------------
def get_session(engine=None):
    """Return a sessionmaker bound to the engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)
