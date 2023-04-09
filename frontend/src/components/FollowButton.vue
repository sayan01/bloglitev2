<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { apiClient } from '@/axios';
import type { UserType } from '@/types/UserType';
const props = defineProps<{
    user: UserType;
}>();
const currentUserFollowsHim = ref(false);
const currentUserIsThisUser = ref(false);

const follow = () => { 
    apiClient.post(`/user/follow/${props.user.id}`)
    .then(() => {
        currentUserFollowsHim.value = true;
    })
};
const unfollow = () => { 
    apiClient.delete(`/user/follow/${props.user.id}`)
    .then(() => {
        currentUserFollowsHim.value = false;
    })
};
const getFollowData = () => {
    if(!props.user.id) return;
    apiClient.get(`/user/follow/${props.user.id}`)
    .then(res => {
        currentUserFollowsHim.value = res.data.followed;
    })
    .catch(err => {
        if(err.response.status === 400) {
            currentUserIsThisUser.value = true;
        }
    });
};
onMounted(async () => {
    // wait as long as props.user.id is undefined
    while(!props.user.id) {
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    getFollowData();
});
</script>

<template>
  <div class="follow-buttons" v-if="!currentUserIsThisUser">
        <button class="btn btn-primary" v-if="!currentUserFollowsHim" @click="follow">Follow</button>
        <button class="btn btn-danger" v-else @click="unfollow">Unfollow</button>
  </div>
    <small v-else class="text-muted">You</small>
</template>

<style scoped lang="scss">

</style>