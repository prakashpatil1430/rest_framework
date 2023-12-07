from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=50)


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    sub = models.CharField(max_length=50)