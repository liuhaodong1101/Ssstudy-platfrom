#from django.shortcuts import render
from django.http import JsonResponse
import json
from StudyApp.models import *
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
import secrets
import uuid
import os
from Ssstudy import settings
import shutil
@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)

        # 判断学生账号是否为8位数字
        if not (data['studentNumber'].isdigit() and len(data['studentNumber']) == 8):
            return JsonResponse({'msg': 'Invalid student number format. It must be an 8-digit number.', 'error_num': 2})

        try:
            # 尝试获取学生对象
            student = Student.objects.get(Sid=data['studentNumber'])
            response = {'msg': 'Has a same Sid student', 'error_num': 1}
        except Student.DoesNotExist:
            Student.objects.create(Sid=data['studentNumber'], Spassword=data['password'], Sname=data['name'])
            response = {'msg': 'success', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating student: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def create_admin(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)

        # 判断管理员账号是否为5位
        if not (data['id'].isdigit() and len(data['id']) == 5):
            return JsonResponse({'msg': 'Invalid admin ID format. It must be a 5-digit number.', 'error_num': 2})

        try:
            # 尝试获取管理员对象
            admin = Admin.objects.get(Aid=data['id'])

            response = {'msg': 'Has a same Aid admin', 'error_num': 1}
        except Admin.DoesNotExist:
            # 如果找不到管理员对象，则创建新的管理员对象
            Admin.objects.create(Aid=data['id'], Apassword=data['password'], Aname=data['name'])
            response = {'msg': 'success', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating admin: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_student_info(request):
    if request.method == 'GET':
        try:
            student_id = request.GET.get('studentNumber')

            # 查询数据库，获取学生信息
            student = Student.objects.get(Sid=student_id)

            # 构建学生信息的字典
            student_info = {
                'Sid': student.Sid,
                'Sname': student.Sname,
                'Semail': student.Semail,
                'Smajor': student.Smajor,
                'Sgrade': student.Sgrade
            }

            return JsonResponse({'student_info': student_info})

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found.'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_student_info(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)

        # 获取学生对象，如果找不到则创建一个新的学生对象

        student = Student.objects.get(Sid=data['Sid'])

        # 更新学生信息
        student.Sname = data['Sname']
        student.Sgrade = data['Sgrade']
        student.Smajor = data['Smajor']
        student.Semail = data['Semail']

        # 保存更新
        student.save()

        return JsonResponse({'message': 'Student information updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

SECRET_KEY = secrets.token_urlsafe(32)

@csrf_exempt
def login_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            student = Student.objects.get(Sid=data['id'])
            if data['password'] == student.Spassword:
                # 生成 JWT 令牌
                token_payload = {
                    'user_id': student.id,
                    'username': student.Sid,
                    'exp': datetime.utcnow() + timedelta(days=30)
                }
                token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
                # 返回带有 token 的响应
                response_data = {
                    'error_num': 0,
                    'msg': 'Login successful',
                    'data': {
                        'token': token,
                        'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': student.Sid,
                            'password': student.Spassword,
                            'name': student.Sname  # 根据实际情况添加其他用户信息
                        },
                        'permissions': [],  # 根据实际情况设置权限列表
                        'roles': []  # 根据实际情况设置角色列表
                    }
                }
                return JsonResponse(response_data)
            else:
                # Incorrect password
                return JsonResponse({'error_num': 1, 'msg': 'Incorrect password'})
        except Student.DoesNotExist:
            # User not found
            return JsonResponse({'error_num': 2, 'msg': 'Student does not exist'})
        except Exception as e:
            return JsonResponse({'error_num': 3, 'msg': 'Error: {}'.format(str(e))})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            admin = Admin.objects.get(Aid=data['id'])
            if data['password'] == admin.Apassword:
                # 生成 JWT 令牌
                token_payload = {
                    'user_id': admin.id,
                    'username': admin.Aid,
                    'exp': datetime.utcnow() + timedelta(days=30)
                }
                token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
                # 返回带有 token 的响应
                response_data = {
                    'error_num': 0,
                    'msg': 'Login successful',
                    'data': {
                        'token': token,
                        'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': admin.Aid,
                            'password': admin.Apassword,
                            'name': admin.Aname  # 根据实际情况添加其他用户信息
                        },
                        'permissions': [],  # 根据实际情况设置权限列表
                        'roles': []  # 根据实际情况设置角色列表
                    }
                }
                return JsonResponse(response_data)
            else:
                # Incorrect password
                return JsonResponse({'error_num': 1, 'msg': 'Incorrect password'})
        except Admin.DoesNotExist:
            # User not found
            return JsonResponse({'error_num': 2, 'msg': 'Admin does not exist'})
        except Exception as e:
            return JsonResponse({'error_num': 3, 'msg': 'Error: {}'.format(str(e))})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_all_communities(request):
    if request.method == 'GET':
        # 获取所有Community对象
        communities = Community.objects.all()

        # 将Community对象列表转换为JSON格式
        community_list = [{'CommunityId': community.CommunityId, 'CommunityName': community.CommunityName, 'Aid': community.Aid} for community in communities]

        return JsonResponse({'error_num':0, 'communities': community_list})
    else:
        return JsonResponse({'error_num':1, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_community_details(request, community_id):
    if request.method == 'GET':
        try:
            community = Community.objects.get(CommunityId=community_id)
            community_data = {
                'CommunityId': community.CommunityId,
                'CommunityName': community.CommunityName,
                'Aid': community.Aid,
                'Aname': Admin.objects.get(Aid=community.Aid).Aname,
            }
            return JsonResponse({'community': community_data})
        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_posts_by_community(request, community_id):
    if request.method == 'GET':
        # 查询指定 CommunityId 下的所有帖子
        posts = Post.objects.filter(CommunityId=community_id)

        # 将日期时间字段转换为字符串，然后将帖子对象列表转换为 JSON 格式
        post_list = [
            {
                'Pid': post.Pid,
                'Sid': post.Sid,
                'Sname': Student.objects.get(Sid=post.Sid).Sname,  # Fix here
                'Ptitle': post.Ptitle,
                'Plabel': post.Plabel,
                'Pcontent': post.Pcontent,
                'Plikes': post.Plikes,
                'CommunityId': post.CommunityId
            }
            for post in posts
        ]

        # 返回帖子信息的 JSON 格式作为响应
        return JsonResponse({'error_num': 0, 'posts': post_list})
    else:
        return JsonResponse({'error_num': 1, 'error': '无效的请求方法。'}, status=400)

@csrf_exempt
def get_posts_by_community_and_plabel(request, community_id, plabel):
    if request.method == 'GET':
        # 查询指定 CommunityId 下的所有帖子
        if plabel:
            posts = Post.objects.filter(CommunityId=community_id, Plabel=plabel)
        else:
            posts = Post.objects.filter(CommunityId=community_id)

        # 将日期时间字段转换为字符串，然后将帖子对象列表转换为 JSON 格式
        post_list = [
            {
                'Pid': post.Pid,
                'Sid': post.Sid,
                'Sname': Student.objects.get(Sid=post.Sid).Sname,  # Fix here
                'Ptitle': post.Ptitle,
                'Plabel': post.Plabel,
                'Pcontent': post.Pcontent,
                'Plikes': post.Plikes,
                'CommunityId': post.CommunityId
            }
            for post in posts
        ]

        # 返回帖子信息的 JSON 格式作为响应
        return JsonResponse({'error_num': 0, 'posts': post_list})
    else:
        return JsonResponse({'error_num': 1, 'error': '无效的请求方法。'}, status=400)

@csrf_exempt
def like_post(request, post_id, user_id):
    try:
        post = Post.objects.get(Pid=post_id)

        # 检查用户是否已经点赞过
        like_exists = StudentPostLike.objects.filter(Sid=user_id, Pid=post_id).exists()

        if like_exists:
            # 如果已经点赞，表示用户要取消点赞
            post.Plikes -= 1
            post.save()
            StudentPostLike.objects.filter(Sid=user_id, Pid=post_id).delete()

            return JsonResponse({'error_num': 0, 'msg': '取消点赞成功'})

        # 进行点赞
        post.Plikes += 1
        post.save()

        StudentPostLike.objects.create(Sid=user_id, Pid=post_id)
        # 记录点赞关系


        return JsonResponse({'error_num': 0, 'msg': '帖子点赞成功'})

    except Post.DoesNotExist:
        return JsonResponse({'error_num': 2, 'msg': '未找到帖子'})
    except Exception as e:
        return JsonResponse({'error_num': 3, 'msg': str(e)})

@csrf_exempt
def get_comments_by_post(request, post_id):
    if request.method == 'GET':
        # 查询指定 PostId 下的所有评论
        comments = Comment.objects.filter(Pid=post_id)

        # 将评论对象列表转换为 JSON 格式
        comment_list = [
            {
                'CommentId': comment.CommentId,
                'Sid': comment.Sid,
                'Sname': Student.objects.get(Sid=comment.Sid).Sname,
                'Pid': comment.Pid,
                'CommentContent': comment.CommentContent,
                'CommentLikes': comment.CommentLikes,
            }
            for comment in comments
        ]

        # 返回评论信息的 JSON 格式作为响应
        return JsonResponse({'error_num': 0, 'comments': comment_list})
    else:
        return JsonResponse({'error_num': 1, 'error': '无效的请求方法。'}, status=400)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)
        app_config, created = AppConfig.objects.get_or_create(pk=1)

        # 判断帖子标题长度是否符合要求
        if len(data['title']) > 30:
            return JsonResponse({'msg': 'Invalid title length. It must be 30 characters or less.', 'error_num': 2})

        pid = app_config.pid
        app_config.pid = pid + 1
        app_config.save()

        try:
            # 创建帖子对象
            Post.objects.create(
                Pid=pid,
                Sid=data['studentNumber'],
                Ptitle=data['title'],
                Plabel=data['label'],
                Pcontent=data['content'],
                Plikes=0,
                CommunityId=data['communityId']
            )
            response = {'msg': 'success', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating post: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def create_community(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)
        app_config, created = AppConfig.objects.get_or_create(pk=1)

        # 判断社区名长度是否符合要求
        if len(data['communityName']) > 20:
            return JsonResponse({'msg': 'Invalid community name length. It must be 20 characters or less.', 'error_num': 2})

        communityId = app_config.communityId
        app_config.communityId = communityId + 1
        app_config.save()

        try:
            # 创建社区对象
            Community.objects.create(
                CommunityId=communityId,
                CommunityName=data['communityName'],
                Aid=data['aid']
            )
            response = {'msg': 'success', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating community: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_post(request, pid, user_id):
    if request.method == 'DELETE':
        try:
            # 查询要删除的帖子
            post_to_delete = Post.objects.get(Pid=pid)

            # 获取帖子的创建者ID
            post_creator_id = post_to_delete.Sid

            # 验证权限
            if len(post_creator_id) == 5 or (len(post_creator_id) == 8 and post_creator_id == user_id):
                # 删除帖子
                post_to_delete.delete()

                response = {'msg': '帖子删除成功', 'error_num': 0}
            else:
                response = {'msg': '无权删除该帖子', 'error_num': 3}

        except Post.DoesNotExist:
            response = {'msg': '未找到帖子', 'error_num': 1}
        except Exception as e:
            response = {'msg': '删除帖子时出错: {}'.format(str(e)), 'error_num': 2}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': '无效的请求方法。'}, status=400)


@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        data = json.loads(request.body)
        app_config, created = AppConfig.objects.get_or_create(pk=1)

        commentId = app_config.commentId
        app_config.commentId = commentId + 1
        app_config.save()

        try:
            # Create a comment object
            Comment.objects.create(
                CommentId=commentId,
                Sid=data['studentNumber'],
                Pid=data['postId'],  # Assuming you have a postId field in the request data
                CommentContent=data['content'],
                CommentLikes=0,
            )
            response = {'msg': 'success', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating comment: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_comment(request, comment_id, user_id):
    if request.method == 'DELETE':
        try:
            # 尝试获取指定 comment_id 的评论
            comment = Comment.objects.get(CommentId=comment_id)

            # 获取评论的创建者ID
            comment_creator_id = comment.Sid

            # 验证权限
            if len(comment_creator_id) == 5 or (len(comment_creator_id) == 8 and comment_creator_id == user_id):
                # 删除评论
                comment.delete()

                response = {'msg': 'success', 'error_num': 0}
            else:
                response = {'msg': '无权删除该评论', 'error_num': 3}

        except Comment.DoesNotExist:
            response = {'msg': '评论不存在', 'error_num': 1}
        except Exception as e:
            response = {'msg': '删除评论时出错: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': '无效的请求方法。'}, status=400)

@csrf_exempt
def get_student_likes(request, student_id):
    if request.method == 'GET':
        try:
            # 根据学生的Sid获取该学生点赞的所有帖子
            liked_posts = StudentPostLike.objects.filter(Sid=student_id).values('Pid')

            # 获取所有点赞的帖子的详细信息
            liked_posts_details = Post.objects.filter(Pid__in=liked_posts)

            # 将结果转换为列表
            liked_posts_list = [
                {
                    'Pid': post.Pid,
                    'Sid': post.Sid,
                    'Ptitle': post.Ptitle,
                    'Plabel': post.Plabel,
                    'Pcontent': post.Pcontent,
                    'Plikes': post.Plikes,
                    'CommunityId': post.CommunityId,
                }
                for post in liked_posts_details
            ]

            return JsonResponse({'liked_posts': liked_posts_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def has_student_liked_post(request, student_id, post_id):
    if request.method == 'GET':
        try:
            # 检查学生和帖子是否存在点赞关系
            has_liked = StudentPostLike.objects.filter(Sid=student_id, Pid=post_id).exists()

            return JsonResponse({'has_liked': has_liked})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def edit_post(request):
    try:
        data = json.loads(request.body)

        post_id = data['postId']
        new_content = data['newContent']
        print(post_id)
        print(new_content)
        # Fetch the post from the database
        post = Post.objects.get(Pid=post_id)

        # Update the post content
        post.Pcontent = new_content
        post.save()

        return JsonResponse({'error_num': 0, 'msg': '帖子内容修改成功'})
    except Post.DoesNotExist:
        return JsonResponse({'error_num': 1, 'msg': '帖子不存在'})
    except Exception as e:
        return JsonResponse({'error_num': 2, 'msg': str(e)})

@csrf_exempt
def get_post_likes(request, post_id):
    if request.method == 'GET':
        try:
            # 获取帖子的点赞数
            post_likes = StudentPostLike.objects.filter(Pid=post_id).count()

            return JsonResponse({'post_likes': post_likes})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_student_posts(request, student_id):
    if request.method == 'GET':
        try:
            # 根据学生的Sid获取该学生发布的所有帖子
            student_posts = Post.objects.filter(Sid=student_id)

            # 将结果转换为列表
            student_posts_list = [
                {
                    'Pid': post.Pid,
                    'Sid': post.Sid,
                    'Ptitle': post.Ptitle,
                    'Plabel': post.Plabel,
                    'Pcontent': post.Pcontent,
                    'Plikes': post.Plikes,
                    'CommunityId': post.CommunityId,
                }
                for post in student_posts
            ]

            return JsonResponse({'student_posts': student_posts_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        data = json.loads(request.body)
        # Assuming you have necessary fields in the request data (e.g., courseId, aid, courseName, courseType)
        app_config, created = AppConfig.objects.get_or_create(pk=1)

        courseId = app_config.courseId
        app_config.courseId = courseId + 1
        app_config.save()
        aid = data['aid']
        courseName = data['courseName']
        courseType = data['courseType']
        courseDescription = data['courseDescription']
        try:
            # Check if the course with the given courseId already exists
            Course.objects.get(CourseId=courseId)
            response = {'msg': 'Course with ID {} already exists.'.format(courseId), 'error_num': 2}
        except Course.DoesNotExist:
            # Create a course object
             folder_path = os.path.join(settings.MEDIA_ROOT, str(courseId))
             os.makedirs(folder_path, exist_ok=True)
             Course.objects.create(
                CourseId=courseId,
                CourseName=courseName,
                CourseType=courseType,
                Aid=aid,
                CourseDescription = courseDescription,
            )
             response = {'msg': 'Course created successfully', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating course: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@csrf_exempt
def get_all_courses(request):
    if request.method == 'GET':
        # 获取所有Community对象
        courses = Course.objects.all()
        # 将Community对象列表转换为JSON格式
        course_list = [{'courseId': course.CourseId, 'courseName': course.CourseName, 'courseType': course.CourseType} for course in courses]

        return JsonResponse({'error_num':0, 'courses': course_list})
    else:
        return JsonResponse({'error_num':1, 'error': 'Invalid request method.'}, status=400)
    

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        app_config, created = AppConfig.objects.get_or_create(pk=1)

        fid = app_config.fid
        app_config.fid = fid + 1
        app_config.save()
        sid = request.POST.get('sid')
        fName = request.POST.get('fName')
        faddr = request.POST.get('faddr')
        courseId = request.POST.get('courseId')
        parts = faddr.split('/')
        # 指定文件保存路径
        file_path = os.path.join(settings.MEDIA_ROOT, parts[1],parts[2])  # Replace 'your_media_root' with your actual media root

        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        try:
            # Create a course object
            File.objects.create(
                Fid=fid,
                FName=fName,
                Faddr=faddr,
                CourseId=courseId,
                Sid = sid,
            )
            response = {'msg': 'Course created successfully', 'error_num': 0}
        except Exception as e:
            response = {'msg': 'Error creating course: {}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    

@csrf_exempt
def delete_course(request):
    if request.method == 'POST':
        # 解析请求中的 JSON 数据
        data = json.loads(request.body)
        courseId = data.get('courseId')

        # 删除数据库中的课程对象
        try:
            course = Course.objects.get(CourseId=courseId)
            # 删除课程对象
            course.delete()

            # 删除文件夹及其内容
            folder_path = os.path.join(settings.MEDIA_ROOT, str(courseId))
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

            response = {'msg': '课程删除成功', 'error_num': 0}
        except Course.DoesNotExist:
            response = {'msg': '课程不存在', 'error_num': 1}
        except Exception as e:
            response = {'msg': '删除课程时出错：{}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': '无效的请求方法。'}, status=400)


@csrf_exempt
def get_files_by_course_id(request):
    if request.method == 'POST':
        # 解析请求中的 JSON 数据
        data = json.loads(request.body)

        # 假设前端传来的数据包含 courseId
        courseId = data.get('courseId')

        if courseId is not None:
            try:
                # 获取指定 CourseId 的所有文件
                files = File.objects.filter(CourseId=courseId)
                course = Course.objects.get(CourseId = courseId)
                # 将文件信息转换为JSON格式
                files_list = [{'fid': file.Fid, 'fName': file.FName, 'faddr': file.Faddr,"sid": file.Sid} for file in files]

                return JsonResponse({'error_num': 0, 'files': files_list,'description' : course.CourseDescription,"courseName" : course.CourseName,"courseType" : course.CourseType})
            except Exception as e:
                return JsonResponse({'error_num': 1, 'error': 'Error retrieving files: {}'.format(str(e))}, status=500)
        else:
            return JsonResponse({'error_num': 1, 'error': 'Missing courseId in the request data.'}, status=400)
    else:
        return JsonResponse({'error_num': 1, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        # 解析请求中的 JSON 数据
        data = json.loads(request.body)
        fid = data.get('fid')

        # 删除数据库中的文件对象
        try:
            file_instance = File.objects.get(Fid=fid)
            # 删除文件对象
            faddr = file_instance.Faddr
            parts = faddr.split('/')
            # 删除文件夹及其内容
            folder_path = os.path.join(settings.MEDIA_ROOT, parts[1],parts[2])
            if os.path.exists(folder_path):
                os.remove(folder_path)
            file_instance.delete()
            response = {'msg': '文件删除成功', 'error_num': 0}
        except File.DoesNotExist:
            response = {'msg': '文件不存在', 'error_num': 1}
        except Exception as e:
            response = {'msg': '删除文件时出错：{}'.format(str(e)), 'error_num': 1}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': '无效的请求方法。'}, status=400)


@csrf_exempt
def get_admin_info(request):
    if request.method == 'GET':
        try:
            admin_id = request.GET.get('adminId')  # 假设管理员ID通过请求参数传递

            # 查询数据库，获取管理员信息
            admin = Admin.objects.get(Aid=admin_id)

            # 构建管理员信息的字典
            admin_info = {  # 假设管理员模型有一个名为 id 的字段用于唯一标识
                'Aname': admin.Aname,
                'Aemail': admin.Aemail,
                'AdminId': admin.Aid
            }

            return JsonResponse({'admin_info': admin_info})

        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def update_admin_info(request):
    if request.method == 'POST':
        # 解析请求的 JSON 数据
        data = json.loads(request.body)

        try:
            # 获取管理员对象，如果找不到则创建一个新的管理员对象
            admin = Admin.objects.get(Aid=data['AdminId'])  # 假设管理员ID通过请求数据传递

            # 更新管理员信息
            admin.Aname = data['Aname']
            admin.Aemail = data['Aemail']

            # 保存更新
            admin.save()

            return JsonResponse({'message': 'Admin information updated successfully.'})

        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)