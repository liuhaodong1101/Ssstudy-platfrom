from django.test import TestCase

# Create your tests here.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ssstudy.settings')
import django
django.setup()

from StudyApp import views

views.create_student("21373453", "fcyfcyzwd9", "fancy")
views.login_student("21373453", "fcyfcyzwd9")
views.student_change_password("21373453", "fcyfcyzwd8")