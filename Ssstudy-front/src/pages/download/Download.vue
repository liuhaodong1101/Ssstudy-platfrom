<template>
  <div>
    <div>

      <div class="scrollable-textbox">
        <p class="bold-text">课程名称：{{ courseName }}</p>
        <p class="bold-text">课程类型：{{ courseType }}</p>
        <p class="bold-text">课程描述：{{ description }}</p>
      </div>

    </div>
    <div class="action-buttons">
      <button class="action-button" @click="uploadFile">上传文件</button>
    </div>
    <div>
      <div class="allFile-container">
        <div class="search-bar">
          <input v-model="searchKeyword" placeholder="搜索文件...">
        </div>
        <!-- <h1>课程文件列表</h1> -->
        <ul>
          <li v-for="file in filteredFiles()" :key="file.fid">
            <div class="file-container">
              <button class="delete-button" @click="deleteFile(file.fid)">×</button>
              <a :href="file.faddr" download>  {{ file.fName }} &nbsp; 上传者id: {{ file.sid }}</a>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 上传文件对话框 -->
    <el-dialog :visible.sync="uploadDialogVisible" title="上传文件" @close="uploadDialogVisible = false">
      <el-form :model="uploadForm" label-position="top">
        <!-- <el-form-item label="文件名称">
          <el-input v-model="newFile.name"></el-input>
        </el-form-item> -->
        <el-form-item>
          <input type="file" ref="fileInput"/>
        </el-form-item>
        <el-form-item  class="dialog-buttons">
          <el-button type="primary" @click="comfirmUploadFile"  >确认上传</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 删除文件对话框 -->
    <el-dialog :visible.sync="deleteDialogVisible" title="" @close="deleteDialogVisible = false">
      <el-row class="dialog-buttons">
        <div class="dialog-title">删除文件</div>
        <el-col :span="12">
          <el-button type="danger" @click="confirmDelete">删除</el-button>
        </el-col>
        <el-col :span="12">
          <el-button type="info" @click="deleteDialogVisible = false" >取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>
<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
  created() {
    this.loadfiles(); // 调用你希望执行的函数
  },
  data() {
    return {
      files: [
        // { id: 1, name: '文件1', url: './index.html' },
        // { id: 2, name: '文件2', url: '/go.txt' },
        // Add more files as needed
      ],
      uploadDialogVisible: false,
      delete_id:"",
      deleteDialogVisible: false,
      newFile: {
        name: "",
      },
      description:'',
      courseName:'',
      courseType:'',
      searchKeyword: '',
    };
  },
  props: {
    // 启用 props 接收路由参数
    id: {
      type: String,
      required: true
    }
  },
  computed: {
    ...mapGetters('account', ['user']),
    formattedDescription() {
      // 将换行符转换为HTML的换行标签
      return this.description.replace(/\n/g, "<br>");
    },
  },
  methods: {
    async loadfiles() {
      // 假设你已经获得了 coursesResponse 数据
      const courseId = this.$route.params.id;
      const postData = {
        courseId:courseId,
      }
      const filesResponse = await axios.post(`http://127.0.0.1:8000/StudyApp/get_files_by_course_id/`,postData);
      // 假设 coursesResponse.data 包含你从后端获取的数据
      const filesList = filesResponse.data.files;
      this.description = filesResponse.data.description;
      this.courseName = filesResponse.data.courseName;
      this.courseType = filesResponse.data.courseType;
      // 使用 map 方法遍历 coursesList 并创建新的 courses 数组
      const files = filesList.map(file => {
        return {
          fName: file.fName,
          fid: file.fid,
          faddr:file.faddr,
          sid: file.sid,
        };
      });
      // 现在 courses 数组已经包含了你希望的数据，可以在组件中使用了
      this.files = files;
    },
    filteredFiles() {
      if (this.searchKeyword.trim() == '') {
        return this.files;
      }
      const keyword = this.searchKeyword.toLowerCase();
      return this.files.filter(file => file.fName.toLowerCase().includes(keyword));
    },
    uploadFile() {
      // 处理上传文件逻辑
      this.uploadDialogVisible = true;
      console.log('上传文件');
    },
    deleteFile(delete_id) {
      // 处理删除文件逻辑
      this.delete_id = delete_id;
      this.deleteDialogVisible = true;
      console.log('删除文件');
    },
    async comfirmUploadFile() {
      const inputFile = this.$refs.fileInput;
      // 处理上传文件逻辑
      if (inputFile.files.length > 0) {
        // 获取文件对象
        const uploadedFile = inputFile.files[0];
        // 获取文件名
        const fileName = uploadedFile.name;
        console.log(fileName);
        console.log(this.files);
        const isFileNameExists = this.files.some(file => file.fName === fileName);
        if (isFileNameExists) {
          alert('已经有相同的文件啦，修改文件名再上传吧');
          inputFile.value = "";
          this.uploadDialogVisible = false;
          this.newFile.name = "";
          return;
        }
        const courseId = this.$route.params.id;
        const faddr = './' + courseId + '/' + fileName;
        const formData = new FormData();

        // 添加文件字段
        formData.append('file', uploadedFile);
        // 添加其他文本字段
        formData.append('fName', fileName);
        formData.append('faddr', faddr);
        formData.append('courseId', courseId);
        formData.append('sid', this.user.id);
        try {
          // 发送 HTTP POST 请求创建新帖子
          const response = await axios.post('http://127.0.0.1:8000/StudyApp/upload_file/', formData);
          // 检查服务器的响应
          if (response.data.error_num === 0) {
            // 如果成功，将新帖子添加到社区的帖子数组中
            // this.community.posts.push(response.data.post);

            window.location.reload();
          } else {
            // 如果出现错误，显示警告或根据需要进行处理
            alert('创建帖子出错：' + response.data.msg);
          }
        } catch (error) {
          console.error('创建帖子出错：', error);
        }
        // 处理上传文件逻辑
        // const newId = Math.max(...this.files.map(file => file.id), 0) + 1;
        // this.files.push(newfile);
        // this.uploadDialogVisible = false;
        // 隐藏对话框
      } else {
        // 用户未选择文件的处理逻辑
        console.log('用户未选择文件');
      }
      // 隐藏对话框
      inputFile.value = "";
      this.uploadDialogVisible = false;
      this.newFile.name = "";
      console.log('上传文件');
    },

    async confirmDelete() {
      // 处理删除文件逻辑
      const postdata = {
        fid:this.delete_id,
      }
      const foundFile = this.files.find(file => file.fid === this.delete_id);
      if (this.user.id.length === 8 && !(foundFile.sid === this.user.id)) {
        alert('你没有权限删除这个文件');
        this.delete_id = "";
        this.deleteDialogVisible = false;
        return;
      }
      try {
        // 发送 HTTP POST 请求创建新帖子
        const response = await axios.post('http://127.0.0.1:8000/StudyApp/delete_file/', postdata);
        // 检查服务器的响应
        if (response.data.error_num === 0) {
          // 如果成功，将新帖子添加到社区的帖子数组中
          window.location.reload();
        } else {
          // 如果出现错误，显示警告或根据需要进行处理
          alert('创建帖子出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('创建帖子出错：', error);
      }
      this.delete_id = "";
      this.deleteDialogVisible = false;
      console.log('删除文件');
    },
  },
  // 在组件中通过 this.id 获取课程的 id
  // ...
};
</script>
<style>

.centered-text p {
  font-size: 18px;
  margin: 5px 0; /* 根据需要调整每行文本的上下边距 */
}
.search-bar {
  text-align: center; /* 居中文本 */
  margin-bottom: 20px; /* 调整上下边距，根据需要调整 */
}

.search-bar input {
  /* 添加或调整样式，根据需要调整位置、大小等属性 */
  width: 200px;
  padding: 5px;
}

.allFile-container {
  overflow-y: auto;
  position: relative; /* Change to relative positioning */
  /* Remove bottom, left, and transform properties */
  display: flex;
  flex-direction: column;
  height: 45vh;
  width: 81%;
  padding: 10px;
  border: 2px solid #333;
  border-radius: 10px;
  background: white;
  margin: 0 auto; /* Center the container */
}





ul {
  font-size: 24px;
  list-style: none;
  padding: 20PX;
}

h1 {
  font-size: 24px;
  margin-bottom: 16px;
}
.delete-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: white;
  color: red;
  border: none;
  padding: 5px;
  cursor: pointer;
  font-size: 16px; /* Adjust the font size according to your preference */
}

.file-container a {
  text-decoration: none;
  color: #333;
}
.file-container {
  position: relative;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.file-container a:hover {
  text-decoration: underline;
}
.action-buttons {
  position: relative; /* Change to relative positioning */
  display: flex;
  justify-content: flex-end; /* Adjust alignment */
  margin-top: 20px;
}
.dialog-buttons {
  text-align: center; /* 将按钮居中对齐 */
  margin-top: 20px; /* 顶部间距，根据需要调整 */
}
.action-button:hover {
  background-color: #66b1ff;
}
.dialog-buttons {
  text-align: center;
  margin-top: 20px;
}

.dialog-title {
  text-align: center;;
  font-size: 18px; /* 根据需要调整字体大小 */
  font-weight: bold; /* 根据需要调整字体粗细 */
  margin-bottom: 100px; /* 根据需要调整与按钮之间的垂直间距 */
}
li {
  margin-bottom: 8px;
}
.action-button {
  padding: 8px 12px;
  margin-right: 8px;
  font-size: 14px;
  background-color: #409eff;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.scrollable-textbox {
  overflow-y: auto;  /* 允许垂直滚动 */
  max-height: 130px; /* 设置最大高度 */
  white-space: pre-line; /* 保留换行符 */
  border: 1px solid #ccc; /* 添加边框样式 */
  padding: 10px; /* 添加内边距 */
  background: white;


}
.bold-text {
  font-weight: bold; /* 设置粗体 */
}

.file-container {
  position: relative;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow 0.3s ease; /* Add smooth transition for the effect */
}

.file-container:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* Apply box-shadow on hover */
  background: lightyellow;
}
</style>
