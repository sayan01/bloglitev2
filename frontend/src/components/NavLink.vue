<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineProps<{
  name: string
  text?: string
}>()
</script>
<template>
  <span class="nav-link">
      <RouterLink :to="{ name: name }">{{ text || name }}</RouterLink>
  </span>
</template>

<style scoped lang="scss">
.nav-link {
  display: inline-block;
  margin: 0 10px;
}
</style>