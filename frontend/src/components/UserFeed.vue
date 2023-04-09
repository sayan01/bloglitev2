<script setup lang="ts">
import type { PostType } from '@/types/PostType';
import PostCard from './PostCard.vue';
import { apiClient } from '@/axios';
import { onMounted, ref } from 'vue';

const posts = ref([] as PostType[]);

const getPosts = () => {
    apiClient.get('/user/feed')
    .then(res => {
        posts.value = res.data;
    })
    .catch(err => {
        console.log(err);
    });
}
onMounted(() => {
    getPosts();
});
</script>

<template>
  <div class="user-feed">
    <h1>Feed</h1>
    <div class="posts d-flex flex-column justify-content-center align-items-center">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>