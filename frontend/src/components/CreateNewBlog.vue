<script setup lang="ts">
import { apiClient } from '@/axios';
import { ref } from 'vue';

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

const create = async () => {
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
        return
      }
      errorMessage.value = 'Error uploading image.'
      console.log(err);
      return
    }
  }
  apiClient.post('/post', {
    title: title.value,
    caption: content.value,
    imageURL,
  }).then(() => {
    successMessage.value = 'Blog created successfully.';
    title.value = '';
    content.value = '';
    image.value = null;
  }) .catch(err => {
    errorMessage.value = err.response.data.message;
  });
};

</script>

<template>
  <div class="create-new-blog">
    <h2>Upload New Blog</h2>      
    <div class="create-form">
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
          <button type="button" class="btn btn-primary" @click.prevent="create">
            <i class="fas fa-upload"></i>
            Create
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped lang="scss">
.create-new-blog {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  h2 {
    font-size: 2rem;
    font-weight: 400;
  }
  button{
    margin: 0 1rem;
    width: 100px;
    border-radius: 100px;
  }
}
</style>