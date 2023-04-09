<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import ProfilePhoto from './ProfilePhoto.vue';

defineProps<{
    user: UserType;
    title?: string;
}>();
</script>

<template>
<div class="profile-details">
    <h1>{{ title ? title : 'Profile' }}</h1>
    <div class="profile-body d-flex flex-row align-items-center justify-content-center">
        <ProfilePhoto :user="user" />
        <div class="name ms-3">
            <h2><strong>{{ user.name }}</strong> (@{{ user.username }})</h2>
        </div>
    </div>
    <p class="mt-3 text-center">{{ user.about }}</p>
</div>
</template>

<style scoped lang="scss">

</style>