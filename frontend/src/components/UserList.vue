<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import SearchResult from './SearchResult.vue';

defineProps<{
    users: UserType[];
}>()
</script>

<template>
    <div class="results">
        <div class="result" v-for="user in users" :key="user.id">
            <SearchResult :user="user" />
        </div>
    </div>
</template>

<style scoped lang="scss">

.result {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    transition: all 0.05s ease-in-out;
    &:hover {
        background-color: #eee;
        transform: scale(1.01);
    }
}
</style>