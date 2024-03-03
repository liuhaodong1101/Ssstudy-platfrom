<template>
  <div class="course-container">
    <div v-for="community in communities" :key="community.CommunityId" @click="redirectToCourseDetails(community.CommunityId)" class="course-item">
      <span class="clickable-course">{{ community.CommunityName }}</span>
    </div>

    <!-- 创建社区表单 -->
    <div v-if="isUserIdEightDigits" class="course-item">
      <input v-model="newCommunityName" placeholder="输入新社区的名称">
      <button @click="createCommunity">创建社区</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters('account', ['user']),
    isUserIdEightDigits() {
      // 判断 user.id 的位数是否为8
      return String(this.user.id).length === 5;
    },
  },
  data() {
    return {
      communities: [],
      newCommunityName: '', // 用于存储新社区的名称
    };
  },
  mounted() {
    // Fetch communities from the backend when the component is mounted
    this.getAllCommunities();
  },
  methods: {
    async getAllCommunities() {
      try {
        // Make a GET request to the backend API
        const response = await axios.get('http://127.0.0.1:8000/StudyApp/get_all_communities');

        // Update the communities data with the response data
        this.communities = response.data.communities;
      } catch (error) {
        console.error('Error fetching communities:', error);
      }
    },
    async createCommunity() {
      if (this.newCommunityName.trim() !== '') {
        try {
          // 发起一个 POST 请求到后端 API 以创建新的社区
          const response = await axios.post('http://127.0.0.1:8000/StudyApp/create_community/', {
            communityName: this.newCommunityName.trim(),
            aid: this.user.id,
            // 其他必要的数据，比如 adminId，可以在这里包括
          });

          console.log('Response from createCommunity:', response.data);

          // 检查来自服务器的响应
          if (response.data.error_num === 0) {
            // 如果社区成功创建，更新前端数据
            const newCommunity = {
              CommunityId: response.data.CommunityId,
              CommunityName: this.newCommunityName.trim(),
              Aid: response.data.Aid, // 根据你的后端响应调整此处
            };

            this.communities.push(newCommunity);
            
            window.location.reload();
            // 清空输入框
            this.newCommunityName = '';
          } else {
            // 处理来自服务器的错误响应
            console.error('创建社区时出错:', response.data.msg);
          }
        } catch (error) {
          // 处理网络或其他错误
          console.error('创建社区时出错:', error);
        }
      }
    },
    redirectToCourseDetails(communityId) {
      // Use Vue Router to navigate to the community details page
      this.$router.push({ name: '社区详情', params: { id: communityId } });
    },
  },
};
</script>

<style scoped>
.course-container {
  display: flex;
  flex-wrap: wrap;
  font-size: 1.7em;
}

.course-item {
  padding: 10px;
  margin: 10px;
  border: 1px solid #ddd;
  background-color: lightyellow;
  cursor: pointer;
  transition: box-shadow 0.3s; /* Add a transition for a smooth effect */
  box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.1); /* Adjust box shadow properties */
}

.course-item:hover {
  background-color: lightcyan;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2); /* Adjust box shadow properties on hover */
}

.clickable-course {
  font-weight: bold;
  color: #007BFF;
}
</style>