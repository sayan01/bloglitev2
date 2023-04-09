<script setup lang="ts">
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const getPost = () => {
  apiClient.get(`/post/${id}`)
  .then(res => {
    title.value = res.data.title;
    content.value = res.data.caption;
  })
  .catch((e) => {
    console.log(e);
  });
}

onMounted(() => {
    getPost();
});

const title = ref('');
const content = ref('');
const image = ref(null as File | null);

const errorMessage = ref('');
const successMessage = ref('');

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files) {
    image.value = files[0];
  }
};

const edit = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  if(!title.value || !content.value) {
    errorMessage.value = 'Please fill in all fields.';
    return;
  }
  let imageURL = '';
  if (image.value) {
    const formData = new FormData();
    formData.append('photo', image.value);
    try{
      const resp = await apiClient.post('/photo', formData, { headers: { 'Content-Type': 'multipart/form-data', }, })
      imageURL = resp.data.path;
    } catch(err:any) {
      if (err.response) {
        errorMessage.value = err.response.data.message;
      } else errorMessage.value = 'Error uploading image.'
      console.log(err);
      return
    }
  }
  apiClient.put('/post/'+id, {
    title: title.value,
    caption: content.value,
    imageURL,
  }).then(() => {
    router.push({ name: 'profile' })
  }) .catch(err => {
    errorMessage.value = err.response.data.message;
  });
};


</script>

<template>
  <div class="edit-post-view">
    <button type="button" class="btn btn-secondary" @click.prevent="$router.back()">
    <i class="fas fa-arrow-left"></i>
    Back
    </button>
    <h1>Edit Post</h1>
      <form action="">
        <div class="input-group mb-3">
          <span class="input-group-text">
            Title
            <span class="text-danger">*</span>
          </span>
          <input type="text" class="form-control" v-model="title" />
        </div>
        <div class="input-group mb-3">
          <span class="input-group-text">
            Content
            <span class="text-danger">*</span>
          </span>
          <textarea class="form-control" v-model="content"></textarea>
        </div>
        <div class="input-group mb-3">
          <span class="input-group-text">Image</span>
          <input type="file" class="form-control" @change="handleFileChange" />
        </div>
        <div class="message">
          <p class="text-danger">{{ errorMessage }}</p>
          <p class="text-success">{{ successMessage }}</p>
        </div>
        <div class="input-group mb-3 d-flex flex-row justify-content-center">
          <button type="button" class="btn btn-primary" @click.prevent="edit">
            <i class="fas fa-upload"></i>
            Edit
          </button>
        </div>
      </form>
  </div>
</template>

<style scoped lang="scss">

</style>