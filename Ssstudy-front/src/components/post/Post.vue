<template>
  <div class="post-box">
    <div class="delete-post">
      <br>
      <button @click="deletePost(post.Pid)"></button>
    </div>
    <h2>{{ post.Ptitle }}</h2>
    <hr>
    <div class="post-container">
      <p class="poster">作者: {{ post.Sname }}</p>
      <p class="post-plabel">标签: {{post.Plabel}}</p>
    </div>
    <br>
    <div class="post-container">
      <button @click="togglePostContent">
        <i :class="showPostContent ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
      </button>

      <p class="likes">
          <button @click="toggleLike" :style="{ backgroundColor: isLiked ? '#00BFFF' : '' }">
              {{  '👍' }} : {{ post.Plikes }}
          </button>
      </p>

    </div>
    <br>

    <!-- Show post content and comments if showPostContent is true -->
    <div v-if="showPostContent">
      <p class="post-content">{{ post.Pcontent }}</p>
      <div v-if="post.modifyAble">
        <div class="edit-post-form">
          <textarea v-model="editedPostContent" rows="5"></textarea>
          <br>
          <button @click="editPost">修改帖子内容</button>
        </div>
      </div>

      <!-- Comment modules -->
      <Comment v-for="(comment, index) in post.comments" :key="index" :comment="comment" />

      <!-- Add Comment form -->
      <div class="add-comment-form">
        <textarea v-model="newCommentContent" placeholder="输入评论内容以添加评论，或输入评论ID以删除评论"></textarea>
        <button @click="addComment">添加评论</button>
        <span style="margin: 0 40px;"></span> <!-- 这里添加了一个间隔 -->
        <button @click="deleteComment(newCommentContent)">删除评论</button>
      </div>


    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Comment from '../Comment/Comment.vue'; // Assuming the Comment component is in the same directory

export default {
  components: {
    Comment,
  },
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('account', ['user']),
    // 其他 computed 属性
  },
  data() {
    return {
      newCommentContent: '', // To store the content of the new comment
      showPostContent: false, // Variable to track whether to show post content
      editedPostContent: '',//
      isLiked: false, // 新增点赞状态
    };
  },
  created() {
    // 在组件创建时调用fetchAndDisplayLikes
    this.fetchAndDisplayLikes();
  },
  methods: {
    editPost() {
      // 验证编辑后的内容是否不为空
      if (this.editedPostContent.trim() === '') {
        alert('请输入修改后的帖子内容。');
        return;
      }

      // 发送 API 请求更新帖子内容
      const editedPostData = {
        postId: this.post.Pid, // 添加帖子ID
        newContent: this.editedPostContent.trim(),
      };
      console.log(editedPostData)
      axios.post('http://127.0.0.1:8000/StudyApp/edit_post/', editedPostData)
        .then(response => {
          if (response.data.error_num === 0) {
            this.post.Pcontent = this.editedPostContent.trim();
            // 重置编辑内容并关闭编辑模式
            this.editedPostContent = '';
            this.showPostContent = false;

            alert('帖子内容修改成功');
            window.location.reload();
          } else {
            alert('修改帖子内容出错：' + response.data.msg);
          }
        })
        .catch(error => {
          console.error('修改帖子内容出错：', error);
        });
    },

    async fetchAndDisplayLikes() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/StudyApp/has_student_liked_post/${this.user.id}/${this.post.Pid}/`);
        console.log(response.data.has_liked)
        this.isLiked = response.data.has_liked;
      } catch (error) {
        console.error('获取点赞状态失败：', error);
      }
    },
    async toggleLike() {
        try {
            await this.fetchAndDisplayLikes();

            const response = await axios.post(`http://127.0.0.1:8000/StudyApp/like_post/${this.post.Pid}/${this.user.id}/`);
            if (response.data.error_num === 0) {
              // 如果点赞成功，切换点赞状态
              this.isLiked = !this.isLiked;
              this.post.Plikes = this.isLiked ? this.post.Plikes + 1: this.post.Plikes - 1;
              if (this.isLiked) {
                alert('点赞成功');
              } else {
                alert('点赞成功');
              }
              window.location.reload();
          } else {
              // 处理错误
              alert('点赞失败：' + response.data.msg);
            }
          } catch (error) {
            console.error('点赞失败：', error);
        }
    },


    async deletePost(postId) {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/StudyApp/delete_post/${postId}/${this.user.id}/`);
        if (response.data.error_num === 0) {
          window.location.reload();
          alert('帖子删除成功');
        } else if (response.data.error_num === 3) {
          alert('您无权删除该帖子');
        } else {
          // 如果出现错误，显示警告或根据需要进行处理
          alert('删除帖子出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('删除帖子出错：', error);
      }
    },

    async deleteComment(commentId) {
      try {
        // 发送 HTTP DELETE 请求删除评论
        const response = await axios.delete(`http://127.0.0.1:8000/StudyApp/comments/delete/${commentId}/${this.user.id}/`);

        // 检查服务器的响应
        if (response.data.error_num === 0) {
          // 如果成功，从帖子的评论数组中移除已删除的评论
          const index = this.post.comments.findIndex(comment => comment.CommentId === commentId);
          if (index !== -1) {
            this.post.comments.splice(index, 1);
          }

          // 可选：执行其他清理操作或更新界面
          // ...
          window.location.reload();

          alert('评论删除成功');
        } else if (response.data.error_num === 3) {
          alert('您无权删除该评论');
        } else {
          // 如果出现错误，显示警告或根据需要进行处理
          alert('删除评论出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('删除评论出错：', error);
      }
    },



    async addComment() {
      // 验证评论内容是否不为空
      if (this.newCommentContent.trim() === '') {
        alert('请输入评论内容。');
        return;
      }

      const newCommentData = {
        studentNumber: this.user.id, // 替换为实际的学生 ID
        postId: this.post.Pid, // 替换为实际的帖子 ID
        content: this.newCommentContent.trim(),
      };

      try {
        // 发送 HTTP POST 请求创建新评论
        const response = await axios.post('http://127.0.0.1:8000/StudyApp/create_comment/', newCommentData);

        // 检查服务器的响应
        if (response.data.error_num === 0) {
          // 如果成功，将新评论添加到帖子的评论数组中
          const newComment = response.data.comment;
          this.post.comments.push(newComment);

          // 清空输入字段
          this.newCommentContent = '';
          window.location.reload();
        } else {
          // 如果出现错误，显示警告或根据需要进行处理
          alert('创建评论出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('创建评论出错：', error);
      }
    },
    togglePostContent() {
      this.showPostContent = !this.showPostContent;
    },
  },
};
</script>

<style scoped>
.post-box {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 15px 0;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
}

.poster, .likes ,.post-plabel{
  color: #555;
  font-weight: bold;
  margin-bottom: 10px;
}

.post-content {
  color: #666;
  margin-bottom: 20px;
}

.add-comment-form {
  margin-top: 20px;
}

.add-comment-form textarea ,.delete-comment textarea{
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

.add-comment-form button, .delete-comment button {
  background-color: #007BFF;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-comment-form button:hover {
  background-color: #0056b3;
}

.poster, .likes  {
  display: inline-block;
  margin-right: 80px; /* 可选：添加一些右边距以调整它们之间的间距 */
}
.likes button {
  border: none;
  cursor: pointer;
  font-size: 18px; /* 调整字体大小以适应大拇指图标 */
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加过渡效果 */
}
.likes button:hover {
  opacity: 0.8; /* 添加透明度以提供视觉反馈 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 悬停时的浮雕效果 */
}

.delete-post {
  position: relative;
}

.delete-post button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.delete-post button::before {
  content: "✕"; /* Unicode character for a cross mark */
  color: red;   /* Color of the cross mark */
  font-size: 20px;
}
.post-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.post-container p {
  margin: 0;
}

.post-content {
  white-space: pre-line; /* 保留换行符 */
}

.edit-post-form textarea {
  width: 100%; /* 或者设置具体的宽度，例如 width: 400px; */
  resize: vertical; /* 如果希望允许垂直调整大小 */
}
</style>
