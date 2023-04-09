<script setup lang="ts">
import type { CommentType } from '@/types/CommentType';
import type { UserType } from '@/types/UserType';
import { apiClient } from '@/axios';
import { onMounted, ref } from 'vue';
import ProfilePhoto from './ProfilePhoto.vue';

const props = defineProps<{
  comment: CommentType;
}>();

const author = ref({} as UserType);

const getAuthor = () => {
  apiClient.get(`/user/${props.comment.author_id}`)
  .then(res => {
    author.value = res.data;
  })
  .catch(err => {
    console.log(err);
  });
}

onMounted(() => {
  getAuthor();
});

</script>

<template>
  <div class="comment">
    <div class="comment-left">
          <ProfilePhoto :user="author" :size="50" />
    </div>
    <div class="comment-right">
      <div class="comment-header">
          <div class="comment-author">
                <strong class="name">{{ author.name }}</strong> (@ {{ author.username }})
          </div>
          <div class="comment-date">
            {{ props.comment.time }}
          </div>
      </div>
      <div class="comment-body">
        {{ props.comment.content }}
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
// beautiful comment using bootstrap only
.comment {
    display: flex;
    flex-direction: row;
    margin: 10px 0;
    .comment-left {
        margin-right: 10px;
    }
    .comment-right {
        display: flex;
        flex-direction: column;
        width: 100%;
        .comment-header {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        .comment-author {
            display: flex;
            flex-direction: row;
            align-items: center;
            .name {
            margin-right: 5px;
            }
        }
        }
        .comment-body {
        margin-top: 5px;
        }
    }
}
</style>