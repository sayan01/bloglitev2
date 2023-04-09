<script setup lang="ts">
import { ref } from 'vue';
import { apiClient } from '@/axios';

const username = ref('');
const password = ref('');
const password2 = ref('');
const name = ref('');
const about = ref('');
const messageError = ref('');
const messageSuccess = ref('');

const register = () => {
    if (password.value != password2.value) {
        messageError.value = 'Passwords do not match';
        messageSuccess.value = '';
        return;
    }
    if(!username.value || !password.value || !name.value || !about.value) {
        messageError.value = 'Please fill in all fields';
        messageSuccess.value = '';
        return;
    }
    apiClient.post('/users', {
        username: username.value,
        password: password.value,
        name: name.value,
        about: about.value,
        photoURL: null,
    }).then(() => {
        messageSuccess.value = 'Registration successful';
        messageError.value = '';
    }).catch(err => {
        messageError.value = err.response.data.message;
        messageSuccess.value = '';
    })
}
</script>

<template>
  <div class="register-view">
    <h1>Register</h1>
    <form>
      <div class="input-group mb-3">
        <span class="input-group-text">Username</span>
        <input type="text" class="form-control" v-model="username" />
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">Password</span>
        <input type="password" class="form-control" v-model="password" />
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">Confirm Password</span>
        <input type="password" class="form-control" v-model="password2" />
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">Name</span>
        <input type="text" class="form-control" v-model="name" />
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">About</span>
        <input type="text" class="form-control" v-model="about" />
      </div>
      <div class="message text-danger mb-3">
        {{ messageError }}
      </div>
      <div class="message text-success mb-3">
        {{ messageSuccess }}
      </div>
      <button type="submit" class="btn btn-primary" @click.prevent="register">Register</button>
    </form>
  </div>
</template>

<style scoped lang="scss">

</style>