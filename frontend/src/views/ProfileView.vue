<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import { RouterLink, useRouter } from 'vue-router';
import ProfileCard from '@/components/ProfileCard.vue';
import UserPosts from '@/components/UserPosts.vue';
import ProfileStats from '@/components/ProfileStats.vue';

const router = useRouter();

const user = ref({} as UserType);

const getProfile = () => {
    apiClient.get('/user')
    .then(res => {
        user.value = res.data;
    })
    .catch(err => {
        if (err.response.status == 401) {
            alert('You are not authorized to access this page. Please login again.');
            router.push('/login');
        }
    });
}

onMounted(() => {
    getProfile();
});
</script>

<template>
  <div class="profile-view">
    <ProfileCard :user="user" />
    <div class="center">
        <RouterLink :to="{name: 'edit-profile'}" class="btn btn-primary">
            <i class="fas fa-pencil-alt    "></i>
            Edit Profile
        </RouterLink>
    </div>
    <hr>
    <ProfileStats :user="user" />
    <div class="d-flex align-items-center justify-content-between">
        <h2>Posts: </h2>
        <button class="btn btn-outline-primary" @click="exportPosts">
            <i class="fas fa-file-export"></i>
            Export Posts
        </button>
    </div>
    <UserPosts :user="user" />
    <hr>
  </div>
</template>

<style scoped lang="scss">
.center{
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>