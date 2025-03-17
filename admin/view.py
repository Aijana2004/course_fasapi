from course_app.db.models import  UserProfile,Category,Course,Certificate,Exam,Lesson,Question
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username,UserProfile.role]
    name = 'User'
    name_plural = 'Users'

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Category'
    name_plural = 'Categories'


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.course_name,Course.price]
    name = 'Course'
    name_plural = 'Courses'


class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.title,]
    name = 'Lesson'
    name_plural = 'Lessons'


class ExamAdmin(ModelView, model=Exam):
    column_list = [Exam.id, Exam.title]
    name = 'Exam'
    name_plural = 'Exams'


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.title]
    name = 'Question'
    name_plural = 'Questions'


class CertificateAdmin(ModelView, model=Certificate):
    column_list = [Certificate.id, Certificate.student_id]
    name = 'Certificate'
    name_plural = 'Certificates'
