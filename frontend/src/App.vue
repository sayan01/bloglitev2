<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
import { setAuthToken } from './axios';
import localstorage from './localstorage';

const token = localstorage.get('token') || null;
setAuthToken(token);
</script>

<template>
  <NavBar />
  <div class="container">
    <RouterView />
  </div>
</template>

<style scoped></style>
