<template>
  <div class="image-container">
    <div class="new-page">
      <button @click="addCourse">添加课程</button>
      <div class="course-container">
        <ul class="course-list">
          <li v-for="course in courses" :key="course.courseId">
            <div class="course-item">
              <button class="delete-button" @click="deleteCourse(course.courseId)">×</button>
              <router-link :to="{ name: '文件下载页', params: { id: course.courseId }}">
                课程名称：<br />{{ course.courseName }} <br /> 课程类型：<br />{{ course.courseType }}<br />
              </router-link>
            </div>
          </li>
        </ul>
      </div>

      <!-- 对话框 -->
      <el-dialog title="添加课程" :visible.sync="isDialogVisible" @close="isDialogVisible = false">
        <el-form label-position="top">
          <el-form-item label="课程名称">
            <el-input v-model="newCourse.courseName"></el-input>
          </el-form-item>
          <el-form-item label="课程类别">
            <el-input v-model="newCourse.courseType"></el-input>
          </el-form-item>
          <el-form-item label="课程描述">
            <el-input type="textarea" v-model="newCourse.courseDescription" :rows="5"></el-input>
          </el-form-item>
          <el-button type="primary" @click="confirmAdd">确认添加</el-button>
        </el-form>
      </el-dialog>

      <!-- 删除课程的id -->
      <el-dialog title="确定要删除吗" :visible.sync="isDialogVisible_delete" @close="isDialogVisible_delete = false">
        <el-row>
          <el-col :span="12">
            <el-button type="danger" @click="confirmDelete">删除</el-button>
          </el-col>
          <el-col :span="12">
            <el-button type="info" @click="isDialogVisible_delete = false">取消</el-button>
          </el-col>
        </el-row>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Vue from 'vue';
import Meta from 'vue-meta';
Vue.use(Meta);

export default {
  created() {
    this.loadCourses();
  },
  name: 'Demo',
  metaInfo: {
    meta: [
      { name: 'Cache-Control', content: 'no-cache, no-store, must-revalidate' },
    ],
  },
  data() {
    return {
      isDialogVisible: false,
      isDialogVisible_delete: false,
      delete_id: "",
      newCourse: {
        courseName: '',
        courseType: '',
        courseDescription: '',
      },
      courses: [],
    };
  },
  computed: {
    ...mapGetters('account', ['user']),
  },
  methods: {
    redirectToCourseDetails(courseId) {
      this.$router.push({ name: '文件下载页', params: { id: courseId } });
    },
    async loadCourses() {
      try {
        const coursesResponse = await axios.get(`http://127.0.0.1:8000/StudyApp/get_all_courses/`);
        const coursesList = coursesResponse.data.courses;
        this.courses = coursesList.map(course => ({
          courseId: course.courseId,
          courseName: course.courseName,
          courseType: course.courseType,
          courseDescription: course.courseDescription,
        }));
      } catch (error) {
        console.error('Error loading courses:', error);
      }
    },
    addCourse() {
      this.isDialogVisible = true;
    },
    deleteCourse(delete_id) {
      this.delete_id = delete_id;
      this.isDialogVisible_delete = true;
    },
    async confirmDelete() {
      const postdata = { courseId: this.delete_id };
      if (this.user.id.length === 8) {
        alert('你没有权限操作，请联系管理员');
        this.delete_id = "";
        this.isDialogVisible_delete = false;
        return;
      }
      try {
        const response = await axios.post('http://127.0.0.1:8000/StudyApp/delete_course/', postdata);
        if (response.data.error_num === 0) {
          window.location.reload();
        } else {
          alert('创建课程出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('创建课程出错：', error);
      }
      this.delete_id = "";
      this.isDialogVisible_delete = false;
    },
    async confirmAdd() {
      if (this.newCourse.courseName.trim() === '' || this.newCourse.courseType.trim() === '') {
        alert('请输入课程名称和类型');
        this.isDialogVisible = false;
        this.newCourse = { courseName: '', courseType: '', courseDescription: '' };
        return;
      }
      if (this.user.id.length === 8) {
        alert('你没有权限操作，请联系管理员');
        this.isDialogVisible = false;
        this.newCourse = { courseName: '', courseType: '', courseDescription: '' };
        return;
      }
      const newCourse = {
        courseId: null,
        courseName: this.newCourse.courseName,
        courseType: this.newCourse.courseType,
        courseDescription: this.newCourse.courseDescription,
        aid: this.user.id,
      };
      try {
        const response = await axios.post('http://127.0.0.1:8000/StudyApp/create_course/', newCourse);
        if (response.data.error_num === 0) {
          this.newCourse = { courseName: '', courseType: '', courseDescription: '' };
          window.location.reload();
        } else {
          alert('创建课程出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('创建课程出错：', error);
      }
      this.isDialogVisible = false;
      this.newCourse = { courseName: '', courseType: '', courseDescription: '' };
    },
  },
};
</script>

<style scoped lang="less">

.new-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.image-container {
  background-image: url('WechatIMG1079.jpeg');
  background-size: cover; /* 适应容器大小 */
  width: 100%;
  height: 100%;
}

.course-container {
  overflow-y: auto;
  position: relative; /* Change to relative positioning */
  /* Remove bottom, left, and transform properties */
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  height: 75vh;
  width: 80%;
  border: 1px solid #ccc;
  background-image: url('WechatIMG1079.jpeg');
  background-size: cover; /* 适应容器大小 */
  align-self: flex-start;
  // background-color: rgba(255, 255, 255, 0.5);
  // background: white;
  font-size: x-large;
  margin: 10px auto; /* Center the container horizontally */
}

// .course-list {
//   padding: 10px;
//   list-style: none;
//   margin: 0;
//   text-align: left;
// }

.course-item {
  position: relative;
  padding: 10px;
  margin-bottom: 10px;
  margin-left: 10px;
  cursor: pointer;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  background-color: white;
  transition: background-color 0.3s ease;
}

.course-item:hover {
  background-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.delete-button {
  position: absolute; /* Change to absolute positioning */
  top: 0px;
  right: 5px;
  background-color: white;
  color: red;
  border: none;
  padding: 0px;
  cursor: pointer;
  font-size: 16px;
}

.button-container {
  position: relative; /* Change to relative positioning */
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

li {
  display: inline-block;
}

li span {
  display: block;
  padding: 10px;
  box-sizing: border-box;
}

button {
  margin-top: 10px;
  padding: 10px;
  background-color: #3498db;
  color: #fff;
  border: none;
  cursor: pointer;
  border-top: 1px solid #ccc;
  align-self: flex-end;
}
</style>