<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import { DEFAULT_PHOTO_URL, DEFAULT_PROFILE_PHOTO_SIZE, PHOTO_URL_PREFIX } from '@/defaults';
const props = defineProps<{
    user: UserType;
    size?: number;
}>()
</script>

<template>
  <div class="profile-photo" :width="size ?? DEFAULT_PROFILE_PHOTO_SIZE">
        <img :src="PHOTO_URL_PREFIX + user.photoURL" v-if="user.photoURL" :width="size ?? DEFAULT_PROFILE_PHOTO_SIZE"/>
        <img :src="DEFAULT_PHOTO_URL + user.username" alt="profile-photo" :width="size ?? DEFAULT_PROFILE_PHOTO_SIZE" v-else>
  </div>
</template>

<style scoped lang="scss">
.profile-photo{
    img{
        aspect-ratio: 1/1;
        object-fit: cover;
        border-radius: 50%;
        border: 1px solid black;
    }
}
</style>