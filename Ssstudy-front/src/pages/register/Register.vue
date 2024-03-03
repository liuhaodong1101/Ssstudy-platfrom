<template>
  <div class="registration-container">
    <form @submit.prevent="register" class="registration-form">
      <label for="studentNumber" class="form-label">账号:</label>
      <input type="text" id="studentNumber" v-model="studentNumber" class="form-input" required>
      <label for="password" class="form-label">密码:  </label>
      <input type="password" id="password" v-model="password" class="form-input" required>
      <label for="name" class="form-label">姓名:  </label>
      <input type="text" id="name" v-model="name" class="form-input" required>

      <div class="checkbox-container">
        <label for="isAdmin" class="form-label">是否为管理员:</label>
        <input type="checkbox" id="isAdmin" v-model="isAdmin" class="form-checkbox">
      </div>

      <button type="submit" class="form-button">注册</button>
      <br>
      <router-link to="/login" class="back-to-login">返回登录界面</router-link>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // 后端地址
  withCredentials: true,
});

export default {
  data() {
    return {
      studentNumber: '',
      password: '',
      name: '',
      isAdmin: false,
    };
  },
  methods: {
    register() {
      if (this.isAdmin) {
        instance.post('/StudyApp/create_admin/', {
          id: this.studentNumber,
          password: this.password,
          name: this.name,
        })
        .then(response => {
          console.log(response.data); 
          if (response.data.error_num == 0) {
            this.showMessage('管理员注册成功', 'success');
            this.navigateToLogin();
          } else if (response.data.error_num == 1) {
            this.showMessage('管理员注册失败：存在重复账号', 'error');
          } else if (response.data.error_num == 2) {
            this.showMessage('管理员注册失败：账号必须为5位数字', 'error');
          }
        })
        .catch(error => {
          this.showMessage('管理员注册失败: ' + error.response.data.msg, 'error');
        });
      } else {
        instance.post('/StudyApp/create_student/', {
          studentNumber: this.studentNumber,
          password: this.password,
          name: this.name,
        })
        .then(response => {
          console.log(response.data); 
          if (response.data.error_num == 0) {
            this.showMessage('学生注册成功', 'success');
            this.navigateToLogin();
          } else if (response.data.error_num == 1) {
            this.showMessage('学生注册失败：存在重复账号', 'error');
          } else if (response.data.error_num == 2) {
            this.showMessage('学生注册失败：账号必须为8位数字', 'error');
          }
        })
        .catch(error => {
          this.showMessage('学生注册失败: ' + error.response.data.msg, 'error');
        });
      }
    },
    showMessage(message, type) {
      this.$message[type](message);
    },
    navigateToLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.registration-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.registration-form {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  background-color: rgba(255, 255, 255, 0.5);
}

.checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 16px;
  box-sizing: border-box;
  background: white;
}

.form-checkbox {
  margin-right: 8px;
}

.form-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.form-button:hover {
  background-color: #45a049;
}

.back-to-login {
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

.registration-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-image: url('E:/hw-Database22/vue-antd-admin/public/注册页背景.jpg'); /* Replace 'path/to/your/image.jpg' with the actual path to your image file */
  background-size: cover; /* Ensures the background image covers the entire container */
}
</style>