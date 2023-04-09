<script setup lang="ts">
import type { UserType } from '@/types/UserType';
import { onMounted, onUnmounted, ref } from 'vue';
import { apiClient } from '@/axios';
import { RouterLink } from 'vue-router';

const props = defineProps<{
    user: UserType,
}>();

const  number_of_posts = ref(0);
const  number_of_followers = ref(0);
const  number_of_following = ref(0);

let intervalID : any;

onMounted( async () => {
    while(!props.user.id)
        await new Promise(resolve => setTimeout(resolve, 100));
    intervalID = setInterval(getStats, 500);
});

onUnmounted(() => {
    clearInterval(intervalID);
});

const getStats = () => {
    apiClient.get(`/user/${props.user.id}/posts`)
    .then(res => {
        number_of_posts.value = res.data.length;
    }) .catch(err => {
        console.log(err);
    });
    apiClient.get(`/user/${props.user.id}/followers`)
    .then(res => {
        number_of_followers.value = res.data.length;
    }) .catch(err => {
        console.log(err);
    });
    apiClient.get(`/user/${props.user.id}/following`)
    .then(res => {
        number_of_following.value = res.data.length;
    }) .catch(err => {
        console.log(err);
    });
}
</script>

<template>
  <div class="profile-stats d-flex align-items-center justify-content-center">
    <div class="stat">
      <h3>{{number_of_posts}}</h3>
      <p>Posts</p>
    </div>
    <div class="stat">
      <h3>{{number_of_followers}}
        </h3>
      <p>Followers
        <RouterLink v-if="props.user && props.user.id" :to="{name: 'followers', params: {id: props.user.id}}"><i class="fas fa-link    "></i></RouterLink>
      </p>
    </div>
    <div class="stat">
      <h3>{{number_of_following}}</h3>
      <p>Following
        <RouterLink v-if="props.user && props.user.id" :to="{name: 'following', params: {id: props.user.id}}"><i class="fas fa-link    "></i></RouterLink>
      </p>
    </div>

  </div>
</template>

<style scoped lang="scss">
.profile-stats{
    width: 100%;
    height: 100px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    .stat{
        width: 33.33%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-right: 1px solid #eee;
        &:last-child{
            border-right: none;
        }
        h3{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 5px;
        }
        p{
            font-size: 1rem;
            font-weight: 400;
            color: #777;
        }
    }
}
</style>