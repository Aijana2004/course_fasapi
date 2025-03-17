from fastapi import FastAPI
from sqladmin import Admin
from .view import UserProfileAdmin,CategoryAdmin,CourseAdmin,CertificateAdmin,ExamAdmin,QuestionAdmin,LessonAdmin
from course_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(ExamAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(CertificateAdmin)