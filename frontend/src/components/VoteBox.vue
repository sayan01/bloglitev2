<script setup lang="ts">
import type { PostType } from '@/types/PostType';
import type { VoteType } from '@/types/VoteType';
import { computed, onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import type { UserType } from '@/types/UserType';


const props = defineProps<{
  post: PostType;
  currentuser: UserType;
}>();

const votes = ref([] as VoteType[]);
const likes = ref(0);
const dislikes = ref(0);
const liked = ref(false);
const disliked = ref(false);

const likedButtonBootstrapClass = computed(() => {
  if (liked.value) {
    return 'btn btn-success';
  } else {
    return 'btn btn-outline-success';
  }
});

const dislikedButtonBootstrapClass = computed(() => {
  if (disliked.value) {
    return 'btn btn-danger';
  } else {
    return 'btn btn-outline-danger';
  }
});

const getVotes = () => {
  apiClient.get(`/post/${props.post.id}/vote`)
  .then(res => {
    votes.value = res.data;
    console.log(votes.value);
    
    for (let i = 0; i < votes.value.length; i++) {
      if (votes.value[i].score ===1) {
        likes.value++;
      } else {
        dislikes.value++;
      }
      if(votes.value[i].author_id === props.currentuser.id) {
        if (votes.value[i].score === 1) {
          liked.value = true;
        } else {
          disliked.value = true;
        }
      }
    }
  })
  .catch(err => {
    console.log(err);
  });
}

const like = () => {
  if (liked.value) {
    apiClient.delete(`/post/${props.post.id}/vote`)
    .then(() => {
      likes.value--;
      liked.value = false;
    })
    .catch(err => {
      console.log(err);
    });
  } else {
    apiClient.post(`/post/${props.post.id}/vote`, {
      score: 1,
      post_id: props.post.id,
    })
    .then(() => {
      likes.value++;
      liked.value = true;
      if (disliked.value) {
        dislikes.value--;
        disliked.value = false;
      }
    })
    .catch(err => {
      console.log(err);
    });
  }
}

const dislike = () => {
  if (disliked.value) {
    apiClient.delete(`/post/${props.post.id}/vote`)
    .then(() => {
      dislikes.value--;
      disliked.value = false;
    })
    .catch(err => {
      console.log(err);
    });
  } else {
    apiClient.post(`/post/${props.post.id}/vote`, {
            score: -1,
            post_id: props.post.id,
    })
    .then(() => {
      dislikes.value++;
      disliked.value = true;
      if (liked.value) {
        likes.value--;
        liked.value = false;
      }
    })
    .catch(err => {
      console.log(err);
    });
  }
}

onMounted( async () => {
  while(!props.post.id)
    await new Promise(resolve => setTimeout(resolve, 100));
  getVotes();
});

</script>

<template>
  <div class="vote-box mt-3">
    <div class="input-group">
        <button :class="likedButtonBootstrapClass" type="button" @click="like" >
            <i class="fas fa-thumbs-up    "></i>
            Like{{ liked ? 'd' : '' }} ({{ likes }})
        </button>
        <button :class="dislikedButtonBootstrapClass" type="button" @click="dislike" >
            <i class="fas fa-thumbs-down    "></i>
            Dislike{{ disliked ? 'd' : '' }} ({{ dislikes }})
        </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.vote-box{
    width: 100%;
}

</style>