<script setup lang="ts">
import { removeToken } from '@/auth';
import { useRouter } from 'vue-router';
const router = useRouter();
const logout = () => {
    removeToken();
    router.push({ name: 'home' });
}
</script>

<template>
    <div>
        <h1>Logout</h1>
        <h2>Are you sure you want to logout?</h2>
        <button class="btn btn-primary me-3 yes" @click="logout">Yes</button>
        <RouterLink :to="{name: 'home'}" class="btn btn-outline-danger cancel">Cancel</RouterLink>
    </div>
</template>

<style scoped lang="scss">
</style>