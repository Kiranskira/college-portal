from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    coursename=models.CharField(max_length=255) 
    fees=models.IntegerField(null=True)

    def __str__(self):
        return self.coursename
    
class Student(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    studentname=models.CharField(max_length=255)
    address=models.CharField(max_length=255) 
    age=models.IntegerField()
    joiningdate=models.DateField()

class Teacher(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='teacher_images/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

def __str__(self):
    return f"{self.fname} {self.lname}"
