<template>
  <div class="student-info">
    <div v-if="isAdmin">
      <!-- 管理员信息展示和编辑部分 -->
      <h2>管理员信息</h2>
      <p>姓名: {{ admin.Aname }}</p>
      <p>工号: {{ admin.AdminId }}</p>
      <p>邮箱: {{ admin.Aemail }}</p>

      <!-- 编辑按钮和编辑表单 -->
      <button @click="toggleEditMode">{{ editing ? '关闭' : '修改' }}</button>

      <div v-if="editing">
        <label for="aname">姓名:</label>
        <input v-model="admin.Aname" id="aname" />
        <br>
        <label for="aemail">邮箱:</label>
        <input v-model="admin.Aemail" id="aemail" type="email" />

        <br>

        <button @click="saveChanges">保存更改</button>
      </div>
    </div>

    <div v-else>
      <!-- 学生信息展示和编辑部分 -->
      <h2>学生信息</h2>
      <p>姓名: {{ student.Sname }}</p>
      <p>学号: {{ student.Sid }}</p>
      <p>年级: {{ student.Sgrade }}</p>
      <p>专业: {{ student.Smajor }}</p>
      <p>邮箱: {{ student.Semail }}</p>

      <!-- 编辑按钮和编辑表单 -->
      <button @click="toggleEditMode">{{ editing ? '关闭' : '修改' }}</button>

      <div v-if="editing">
        <label for="sname">姓名:</label>
        <input v-model="student.Sname" id="sname" />
        <br>
        <label for="sgrade">年级:</label>
        <input v-model.number="student.Sgrade" id="sgrade" type="number" />
        <br>
        <label for="smajor">专业:</label>
        <input v-model="student.Smajor" id="smajor" />
        <br>
        <label for="semail">邮箱:</label>
        <input v-model="student.Semail" id="semail" type="email" />

        <br>

        <button @click="saveChanges">保存更改</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // 后端地址
  withCredentials: true,
});

export default {
  data() {
    return {
      userIsAdmin: false,
      admin: {
        AdminId: '',
        Aname: '',
        Aemail: '',
      },
      student: {
        Sid: '',
        Sname: '',
        Sgrade: null,
        Smajor: '',
        Semail: '',
      },
      editing: false,
    };
  },
  computed: {
    ...mapGetters('account', ['user']),
    // 其他 computed 属性
  },
  mounted() {
    // 组件加载时获取学生信息
    this.fetchUserInfo();
  },
  methods: {
    toggleEditMode() {
      this.editing = !this.editing;
    },
    fetchUserInfo() {
      const userId = this.user.id;  // 通过路由参数获取用户ID

      if (userId.length === 5) {
        // 如果是管理员，调用获取管理员信息的接口
        instance.get('/StudyApp/get_admin_info/', {
          params: {
            adminId: userId,
          },
        })
            .then(response => {
              this.isAdmin = true;
              this.admin = response.data.admin_info;
            })
            .catch(error => {
              console.error('获取管理员信息时出错:', error.response.data.error);
            });
      } else if (userId.length === 8) {
        // 如果是学生，调用获取学生信息的接口
        instance.get('/StudyApp/get_student_info/', {
          params: {
            studentNumber: userId,
          },
        })
            .then(response => {
              this.isAdmin = false;
              this.student = response.data.student_info;
            })
            .catch(error => {
              console.error('获取学生信息时出错:', error.response.data.error);
            });
      } else {
        console.error('用户ID不合法');
      }
    },
    saveChanges() {
      if (this.isAdmin) {
        // 发送更新管理员信息的请求
        instance.post('/StudyApp/update_admin_info/', this.admin)
            .then(response => {
              console.log('管理员信息更改已保存:', response.data.message);
              this.editing = false;
            })
            .catch(error => {
              console.error('保存更改时出错:', error.response.data.error);
            });
      } else {
        // 发送更新学生信息的请求
        instance.post('/StudyApp/update_student_info/', this.student)
            .then(response => {
              console.log('学生信息更改已保存:', response.data.message);
              this.editing = false;
            })
            .catch(error => {
              console.error('保存更改时出错:', error.response.data.error);
            });
      }
    },
  }
};
</script>

<style scoped>
.student-info {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-family: '黑体', 'SimHei', sans-serif;
  background-color: #fff;
}
.student-info {
  font-size: 1.7em; /* Adjust the font size as needed */
}
p {
  border-bottom: 1px solid #ccc;
  padding-bottom: 5px; /* Add some spacing between the text and the border */
  margin-bottom: 10px; /* Add some spacing between paragraphs */
}

label {
  display: block; /* Ensure labels are on their own line */
  margin-bottom: 5px; /* Add some spacing between labels */
}

input {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}

button {
  padding: 8px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>
