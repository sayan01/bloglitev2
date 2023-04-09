<script setup lang="ts">
import type { PostType } from '@/types/PostType';
import type { UserType } from '@/types/UserType';
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import ProfilePhoto from './ProfilePhoto.vue';
import CommentBox from './CommentBox.vue';
import VoteBox from './VoteBox.vue';
import { PHOTO_URL_PREFIX } from '@/defaults';
const props = defineProps<{
  post: PostType;
}>();
const author = ref({} as UserType);

const currentuser = ref({} as UserType);

const getCurrentUser = async () => {
  const { data } = await apiClient.get('/user');
  currentuser.value = data;
};

const getAuthor = async () => {
  const { data } = await apiClient.get(`/user/${props.post.author_id}`);
  author.value = data;
};

const deleteBlog = async () => {

    const response = confirm('Are you sure you want to delete this blog?');
    if(!response) return;
    apiClient.delete('/post/' + props.post.id)
        .then(() => {
            window.location.reload();
        })
        .catch(err => {
            console.log(err);
        });
};
onMounted(() => {
    getCurrentUser();
    getAuthor();
});

</script>

<template>
  <div class="post-card" v-if="post">
    <div class="post-header d-flex align-items-center gap-3 justify-content-start">
        <ProfilePhoto :v-if-="author != null" :user="author!" :size="70" />
        <div class="header">
            <h2>{{ post.title }}</h2>
            <p class="text-muted" v-if="author">By 
                <RouterLink v-if="author && author.id" :to="{name: 'explore', params: {id: author.id}}">@{{ author.username }} </RouterLink>
                on {{ post.time }}</p>
        </div>
    </div>
    <div class="post-body d-flex align-items-center">
        <div class="post-image" v-if="post.imageURL">
            <img :src="PHOTO_URL_PREFIX + post.imageURL" alt="Post Image" class="img-fluid post-photo">
        </div>
        <div class="post-caption">
            <p v-html="post.caption"></p>
        </div>
    </div>
    <div class="post-footer mt-3" v-if="currentuser && currentuser.id == post.author_id">
        <div class="d-flex justify-content-end">
            <RouterLink :to="{name: 'editpost', params: {id: post.id}}" class="btn btn-primary">
                <i class="fas fa-pencil-alt    "></i>
                Edit
            </RouterLink>
          <button type="button" class="btn btn-outline-danger" @click.prevent="deleteBlog">
            <i class="fas fa-trash"></i>
            Delete Blog
          </button>
        </div>
    </div>
    <VoteBox :post="post" :currentuser="currentuser" />
    <CommentBox :post="post" />
</div>
</template>

<style scoped lang="scss">
.post-card{
    border: 1px solid #ccc;
    width: clamp(300px, 50%, 800px);
    border-radius: 5px;
    padding: 1rem;
    margin-bottom: 1rem;
    .post-body{
        .post-image{
            width: 50%;
            img{
                width: 100%;
                aspect-ratio: 1/1;
                object-fit: cover;
                border-radius: 15px;
            }
        }
        .post-caption{
            font-size: larger;
            margin: auto;
        }
    }
    .post-footer{
        display: flex;
        align-items: center;
        justify-content: center;
    }
}
</style>