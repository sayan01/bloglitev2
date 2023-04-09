<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { UserType } from '@/types/UserType';
import { apiClient } from '@/axios';
import UserList from '@/components/UserList.vue';

const users = ref([] as UserType[]);
const filteredusers = ref([] as UserType[]);
const searchInput = ref('');
const search = () => {
  filteredusers.value = users.value.filter(user => user.username.includes(searchInput.value) || user.name.includes(searchInput.value));
}

onMounted(() => {
    apiClient.get('/users')
    .then(res => {
        users.value = res.data;
        filteredusers.value = users.value;
    })
    .catch(err => {
        console.log(err);
    });
});

</script>

<template>
  <div class="search-view">
    <h1>Search</h1>
    <form action="" class="search-form">
        <div class="input-group mb-3">
            <span class="input-group-text">Search Query:</span>
            <input type="text" class="form-control" v-model="searchInput" />
            <button @click.prevent="search" class="btn btn-primary">Search</button>
        </div>
    </form>
    <UserList :users="filteredusers" />
  </div>
</template>

<style scoped lang="scss">
</style>