<script setup lang="ts">
import type { PostType } from '@/types/PostType';
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import type { CommentType } from '@/types/CommentType';
import CommentItem from './CommentItem.vue';

const props = defineProps<{
    post : PostType;
}>();

const content = ref('');

const commentList = ref([] as CommentType[]);

const addComment = () => {
    apiClient.post(`/post/${props.post.id}/comment`, {
        content: content.value,
        post_id: props.post.id
    })
    .then(res => {
        // add comment to the list at the top
        commentList.value.unshift(res.data);
        content.value = '';
    })
}

const getCommentList = () => {
    apiClient.get(`/post/${props.post.id}/comment`)
    .then(res => {
        commentList.value = res.data;
    })
}

onMounted(() => {
    getCommentList();
});

</script>

<template>
  <div class="comment-box">
    <div class="add-comment">
        <div class="input-group mt-3">
            <input type="text" v-model="content" placeholder="Add a comment..." class="form-control"/>
            <button class="btn btn-outline-primary" @click.prevent="addComment">
                <i class="fas fa-paper-plane    "></i>
                Comment
            </button>
        </div>
    </div>
    <div class="list-of-comments">
        <CommentItem v-for="comment in commentList" :key="comment.id" :comment="comment" />
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>