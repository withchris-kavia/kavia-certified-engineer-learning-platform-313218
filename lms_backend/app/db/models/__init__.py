"""ORM models for the LMS backend.

Importing this module registers models with SQLAlchemy metadata.
"""

from app.db.models.base import Base
from app.db.models.course import Course
from app.db.models.enrollment import Enrollment
from app.db.models.lesson import Lesson
from app.db.models.progress import LessonProgress
from app.db.models.user import User

__all__ = [
    "Base",
    "User",
    "Course",
    "Lesson",
    "Enrollment",
    "LessonProgress",
]
