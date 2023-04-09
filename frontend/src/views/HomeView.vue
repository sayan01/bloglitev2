<script setup lang="ts">
import { onMounted, ref } from 'vue';
import {apiClient} from '@/axios'
import type { UserType } from '@/types/UserType';
import CreateNewBlog from '@/components/CreateNewBlog.vue'
import UserFeed from '@/components/UserFeed.vue';

const user = ref({} as UserType)

const uploadBlog = ref(false)
const toggleUploadBlog = () => {
  uploadBlog.value = !uploadBlog.value
}

const getUserData = async () => {
  const { data } = await apiClient.get('/user');
  user.value = data;
}

onMounted(()=>{
  getUserData();
})
</script>

<template>
  <div class="home-view">
    <h1>Home Feed</h1>
    <h2 class="text-muted">Hello {{ user.name }} (@{{ user.username }})</h2>
    <hr>
    <div class="upload-blog-true" v-if="uploadBlog">
      <CreateNewBlog />
      <hr>
    </div>
    <div class="toggle-button">
      <button class="btn btn-outline-primary" @click="toggleUploadBlog">
        <span v-if="!uploadBlog">Upload Blog</span>
        <span v-else>Hide Upload Box</span>
      </button>
    </div>
    <UserFeed  />
  </div>
</template>

<style scoped lang="scss">
.toggle-button {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>