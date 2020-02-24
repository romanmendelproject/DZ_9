from django.contrib.auth.models import User
from django.db import models
from datetime import date
class PersonMixin(models.Model):
    SEX_MAN = 0
    SEX_WOMAN = 1
    SEX_CHOICES = (
    (SEX_MAN, 'Man'),
    (SEX_WOMAN, 'Woman')
    )
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, default=SEX_MAN)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, default=date.today)
    city = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Teacher(PersonMixin):
    bio = models.CharField(max_length=1000)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.full_name


class Student(PersonMixin):

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.full_name


class Course(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="course")
    students = models.ManyToManyField(Student, related_name="course")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    date = models.DateField(blank=True, default=date.today)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")

    def __str__(self):
        return self.title