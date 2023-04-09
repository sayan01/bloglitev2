<script setup lang="ts">
import { ref } from 'vue'
import { setToken } from '@/auth';
import { apiClient } from '@/axios';
import {useRouter} from 'vue-router'
const router = useRouter()

const username = ref('')
const password = ref('')
const message = ref('')

const login = () => {
    apiClient.post('/user/login', {
        username: username.value,
        password: password.value,
    })
    .then(res => {
        setToken(res.data.access_token)
        router.push('/')
    })
    .catch(err => {
        message.value = err.response.data.message
    })
}

</script>

<template>
    <div class="login-view">
        <h1>Login</h1>
        <form>
            <div class="input-group mb-3">
                <span class="input-group-text">Username</span>
                <input type="text" class="form-control" v-model="username" />
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">Password</span>
                <input type="password" class="form-control" v-model="password" />
            </div>
            <div class="message text-danger mb-3">
                {{ message }}
            </div>
            <button type="submit" class="btn btn-primary" @click.prevent="login">Login</button>
        </form>
    </div>
</template>

<style scoped lang="scss">
</style>