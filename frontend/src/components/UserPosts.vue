<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { UserType } from '@/types/UserType';
import type { PostType } from '@/types/PostType';
import { apiClient } from '@/axios';
import PostCard from './PostCard.vue';

const props = defineProps<{
    user: UserType;
}>();
const posts = ref([] as PostType[]);
const getPosts = () => {
    apiClient.get(`/user/${props.user.id}/posts`)
    .then(res => {
        posts.value = res.data;
    })
    .catch(err => {
        console.log(err);
    });
}
onMounted( async () => {
    while(!props.user.id)
        await new Promise(resolve => setTimeout(resolve, 100));
    getPosts();
});
</script>

<template>
  <div class="user-posts">
    <div class="posts d-flex flex-column justify-content-center align-items-center">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>