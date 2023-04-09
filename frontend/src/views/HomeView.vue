<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'
import {apiClient} from '@/axios'

const router = useRouter()
const data = ref({})
const loadData = () => {

  apiClient.get('/user')
    .then(res => {
      data.value = res.data
    })
    .catch(err => {
      if (err.response.status == 401) {
        alert('You are not authorized to access this page. Please login again.')
        router.push('/login')
      }
    })
}
onMounted(()=>{
  loadData();
})
</script>

<template>
  <main>Hello</main>
  <div class="data">
    {{ data }}
  </div>
</template>
