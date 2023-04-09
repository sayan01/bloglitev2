<script setup lang="ts">
import { useRoute } from 'vue-router';
import { onMounted, onUnmounted, ref } from 'vue';
import type { UserType } from '@/types/UserType';
import { apiClient } from '@/axios';
import UserList from '@/components/UserList.vue';

const route = useRoute();
const id = route.params.id;
const user = ref({} as UserType);
const users = ref([] as UserType[]);

let intervalID : any = null;

const getUser = () => {
  apiClient.get(`/user/${id}`)
  .then(res => {
    user.value = res.data;
  })
  .catch((e) => {
    console.log(e);
  });
}
const getFollowers = () => {
  apiClient.get(`/user/${user.value.id}/followers`)
  .then(res => {
    users.value = res.data;
  })
  .catch((e) => {
    console.log(e);
  });
}
onMounted(() => {
    getUser();
    intervalID = setInterval(getFollowers, 500);
});

onUnmounted(() => {
    clearInterval(intervalID);
});

</script>

<template>
  <div class="followers-view">
    <h1>Followers of @{{ user.username }}</h1>
    <UserList :users="users" />
  </div>
</template>

<style scoped lang="scss">

</style>