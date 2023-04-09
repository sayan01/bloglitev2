<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import ProfilePhoto from './ProfilePhoto.vue';
import FollowButton from './FollowButton.vue';
defineProps<{
    user: UserType;
}>();
</script>

<template>
    <div class="result-body d-flex flex-row align-items-center justify-content-between">
        <div class="left d-flex flex-row align-items-center justify-content-start">
            <ProfilePhoto :user="user" :size="80" />
            <div class="name ms-3">
                <h4><strong>{{ user.name }}</strong> (@{{ user.username }})</h4>
            </div>
        </div>
        <FollowButton :user="user" />
    </div>

</template>

<style scoped lang="scss">

.result-body {
    .result-photo {
        img {
            width: 80px;
            aspect-ratio: 1/1;
            object-fit: cover;
            border-radius: 50%;
        }
    }
}
</style>