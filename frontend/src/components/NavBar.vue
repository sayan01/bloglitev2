<script setup lang="ts">
import NavLink from './NavLink.vue'
import { token } from '@/auth';
</script>
<template>
  <nav>
    <div class="token" v-if="token">
      <NavLink name="home" />
      <NavLink name="profile" />
      <NavLink name="logout" />
    </div>
    <div class="no-token" v-else>
      <NavLink name="login" />
      <NavLink name="register" />
    </div>
  </nav>
</template>
