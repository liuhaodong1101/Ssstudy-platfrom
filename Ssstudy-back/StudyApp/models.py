from django.db import models
from django.utils import timezone

class Student(models.Model):
    Sid = models.CharField(max_length=8)
    Spassword = models.CharField(max_length=20)
    Sname = models.CharField(max_length=10)
    Semail = models.CharField(max_length=100, null=True)
    Smajor = models.CharField(max_length=20, null=True)
    Sgrade = models.IntegerField(null=True)

class Admin(models.Model):
    Aid = models.CharField(max_length=5)
    Apassword = models.CharField(max_length=20)
    Aname = models.CharField(max_length=10)
    Aemail = models.CharField(max_length=100, null=True)

class Course(models.Model):
    CourseId = models.CharField(max_length=30)
    CourseName = models.CharField(max_length=20)
    CourseType = models.CharField(max_length=10)
    CourseDescription = models.CharField(max_length=200, null=True)
    Aid = models.CharField(max_length=8)

class File(models.Model):
    Fid = models.CharField(max_length=30)
    FName = models.CharField(max_length=20)
    Faddr = models.CharField(max_length=200)
    CourseId = models.CharField(max_length=10)
    Sid = models.CharField(max_length=8)

class Community(models.Model):
    CommunityId = models.CharField(max_length=30)
    CommunityName = models.CharField(max_length=20)
    Aid = models.CharField(max_length=8)

class AppConfig(models.Model):
    pid = models.IntegerField(default=1)
    commentId = models.IntegerField(default=1)
    fid = models.IntegerField(default=1)
    communityId = models.IntegerField(default=1)
    iid = models.IntegerField(default=1)
    courseId = models.IntegerField(default=1)

class Post(models.Model):
    Pid = models.CharField(max_length=30)
    Sid = models.CharField(max_length=8)
    Ptitle = models.CharField(max_length=30)
    Plabel = models.CharField(max_length=10, null=True)
    Pcontent = models.CharField(max_length=500)
    Plikes = models.IntegerField(default=0)
    CommunityId = models.CharField(max_length=30)


class Image(models.Model):
    Iid = models.CharField(max_length=30)
    Iname = models.CharField(max_length=30, null=True)
    Iaddr = models.CharField(max_length=200)
    Pid = models.CharField(max_length=30)

class Comment(models.Model):
    CommentId = models.CharField(max_length=30)
    Sid = models.CharField(max_length=8)
    Pid = models.CharField(max_length=30)
    CommentContent = models.CharField(max_length=200)
    CommentLikes = models.IntegerField(default=0)

class CommunityStudent(models.Model):
    CommunityId = models.CharField(max_length=30)
    Sid = models.CharField(max_length=8)
    ifAssist = models.BooleanField()

class StudentPostLike(models.Model):
    Sid = models.CharField(max_length=8)
    Pid = models.CharField(max_length=30)

# Create your models here.
