<template>
  <div class="community-container">
    <div v-if="community.showAddPost">
      <h1 class="community-title">{{ community.communityName }}</h1>
      <div class="admins-container">
        <h2 class="admins-title">Admin: {{ community.aid }}</h2>
      </div>
    </div>
    <div class="search-container">
      <label for="searchQuery">搜索帖子：</label>
      <input v-model="searchQuery" id="searchQuery" placeholder="输入标签搜索帖子">
      <button @click="searchPosts">搜索</button>
    </div>
    <div class="posts-container">
      <Post v-for="(post, index) in community.posts" :key="index" :post="post" />
    </div>
    <!-- Add Post form -->
    <div v-if="community.showAddPost">
      <div class="add-post-container">
        <h2>发表新帖</h2>
        <label for="postTitle">标题：</label>
        <input v-model="newPost.Ptitle" id="postTitle" placeholder="输入帖子标题">

        <label for="postTags">标签：</label>
        <input v-model="newPost.Plabel" id="postTags" placeholder="输入标签">

        <label for="postContent">内容：</label>
        <textarea v-model="newPost.Pcontent" id="postContent" placeholder="输入帖子内容"></textarea>

        <button @click="addPost">发表帖子</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Post from "@/components/post/Post.vue";

export default {
  components: { Post },
  props: {
    community: {
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
      newPost: {
        Ptitle: '',
        Plabel: '',
        Pcontent: '',
      },
      searchQuery: '',
    };
  },
  methods: {
    async addPost() {
      // 验证必填字段是否不为空
      if (this.newPost.Ptitle.trim() === '' || this.newPost.Pcontent.trim() === '') {
        alert('请输入帖子标题和内容。');
        return;
      }

      const postData = {
        Pid: null, // 假设 Pid 将由服务器生成
        studentNumber: this.user.id, // 你可以自定义添加帖子的管理员名称
        title: this.newPost.Ptitle.trim(),
        label: this.newPost.Plabel.trim(),
        content: this.newPost.Pcontent.trim(),
        communityId: this.$route.params.id,
      };

      try {
        // 发送 HTTP POST 请求创建新帖子
        const response = await axios.post('http://127.0.0.1:8000/StudyApp/create_post/', postData);

        // 检查服务器的响应
        if (response.data.error_num === 0) {
          // 如果成功，将新帖子添加到社区的帖子数组中
          this.community.posts.push(response.data.post);

          // 清空输入字段
          this.newPost = {
            Ptitle: '',
            Plabel: '',
            Pcontent: '',
          };
          window.location.reload();
        } else {
          // 如果出现错误，显示警告或根据需要进行处理
          alert('创建帖子出错：' + response.data.msg);
        }
      } catch (error) {
        console.error('创建帖子出错：', error);
      }
    },
    async searchPosts() {
      if (!this.searchQuery.trim()) {
        const postsResponse = await axios.get(`http://127.0.0.1:8000/StudyApp/get_posts_by_community/${this.community.id}`);

        // 输出响应信息
        console.log(postsResponse);

        // 更新帖子数组
        this.$set(this.community, 'posts', postsResponse.data.posts);
        return;
      }

      try {
        const postsResponse = await axios.get(`http://127.0.0.1:8000/StudyApp/get_posts_by_community_and_plabel/${this.community.id}/${this.searchQuery}`);

        // 输出响应信息
        console.log(postsResponse);

        // 更新帖子数组
        this.$set(this.community, 'posts', postsResponse.data.posts);

        // 可以在这里执行额外的搜索操作
      } catch (error) {
        console.error('搜索帖子出错：', error);
      }
    },

  },
};
</script>

<style scoped>
.community-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-size: 1.2em;
}

/* ... (existing styles) ... */

.add-post-container {
  margin-top: 21px;
}

.add-post-container h2 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.add-post-container label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #555;
}

.add-post-container input,
.add-post-container textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
}

.add-post-container button {
  padding: 10px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  cursor: pointer;
}

.add-post-container button:hover {
  background-color: #0056b3;
}
</style>