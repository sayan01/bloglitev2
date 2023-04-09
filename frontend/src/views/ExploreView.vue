<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import ProfileCard from '@/components/ProfileCard.vue';
import FollowButton from '@/components/FollowButton.vue';
import UserPosts from '@/components/UserPosts.vue';
import ProfileStats from '@/components/ProfileStats.vue';

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const user = ref({} as UserType);

const getUser = () => {
  apiClient.get(`/user/${id}`)
  .then(res => {
    user.value = res.data;
  })
  .catch(() => {
    router.push({name: 'profile'})
  });
}

onMounted(() => {
  getUser();
});

</script>

<template>
  <div class="exploreview">
    <ProfileCard :user="user" title="Explore"/>
    <div class="center">
      <FollowButton :user="user" />
    </div>
    <hr>
    <ProfileStats :user="user" />
    <h2>Posts:</h2>
    <UserPosts :user="user" />
  </div>
</template>

<style scoped lang="scss">

.center{
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>