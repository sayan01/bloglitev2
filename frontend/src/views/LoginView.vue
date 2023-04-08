<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const login = () => {
    console.log('login', username.value, password.value)
}

</script>

<template>
    <div class="login-view">
        <h1>Login</h1>
        <form>
            <div class="input-group">
                <span class="input-group-text">Username</span>
                <input type="text" class="form-control" />
            </div>
            <div class="input-group">
                <span class="input-group-text">Password</span>
                <input type="password" class="form-control" />
            </div>
            <button type="submit" class="from-control">Login</button>
        </form>
    </div>
</template>

<style scoped lang="scss">
</style>