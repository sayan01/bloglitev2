<script setup lang="ts">
import { ref } from 'vue'
import localstorage from '@/localstorage';
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
        localstorage.set('token', res.data.access_token)
        router.push('/')
    })
    .catch(err => {
        if(err.response.status == 404) {
            message.value = 'Username does not exist'
        }
        else if(err.response.status == 403) {
            message.value = 'Incorrect password'
        }
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