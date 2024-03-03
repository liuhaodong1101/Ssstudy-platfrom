<!-- Comment.vue -->
<template>
  <div class="comment-box">
    <p class="comment-id">ID: {{comment.CommentId}}</p>
    <p class="commenter">学号: {{ comment.Sid }} 姓名：{{comment.Sname}}</p>
    <hr>
    <p class="comment-content">{{ comment.CommentContent }}</p>
  </div>
</template>

<script>
export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.comment-box {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
  background-color: #f8f8f8;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.commenter {
  color: #007BFF;
  font-weight: bold;
}

.comment-content {
  color: #333;
  white-space: pre-line; /* 保留换行符 */
}
</style>
