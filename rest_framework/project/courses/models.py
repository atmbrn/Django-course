from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.experience_years} yrs)"


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    instructor = models.ForeignKey(
        Instructor, on_delete=models.PROTECT, related_name="courses"
    )
    students = models.ManyToManyField(Student, related_name="courses", blank=True)

    def __str__(self):
        return self.title
