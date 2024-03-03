<!-- YourComponent.vue -->
<template>
  <div>
    <Community :community="myCommunity"></Community>
  </div>
</template>

<script>
import axios from 'axios';
import Community from "@/components/community/Community.vue";

export default {
  components: {
    Community,
  },
  data() {
    return {
      myCommunity: null,
    };
  },
  created() {
    this.fetchData(1);
  },
  methods: {
    async fetchData(communityId) {
      try {
        // 获取帖子数据
        const postsResponse = await axios.get(`http://127.0.0.1:8000/StudyApp/get_posts_by_community/${communityId}`);
        console.log(postsResponse);
        // 获取评论数据
        await this.fetchComments(postsResponse.data.posts);
        // 将所有帖子赋值给 myCommunity.posts，并添加Community的详细信息
        this.myCommunity = {
          id: 0,
          posts: postsResponse.data.posts,
          communityName:"你点赞的帖子",
          aid: 0,
          showAddPost: false,
        };
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async fetchComments(posts) {
      // 获取每个帖子的评论
      for (const post of posts) {
        post.modifyAble = true;
        const commentsResponse = await axios.get(`http://127.0.0.1:8000/StudyApp/get_comments_by_post/${post.Pid}`);
        console.log(commentsResponse);

        // 将评论赋值给相应的帖子
        post.comments = commentsResponse.data.comments;
      }
    },
  },
};
</script>
