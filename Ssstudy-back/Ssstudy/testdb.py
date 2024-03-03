from django.http import HttpResponse

import StudyApp
from StudyApp.models import *
from StudyApp.views import *


# 数据库操作
def testdb(request):
    return HttpResponse("<p>数据添加成功！</p>")