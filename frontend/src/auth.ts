// src/auth.js
import { ref } from 'vue';
import localstorage from '@/localstorage';

const token = ref(localstorage.get('token'));

function setToken(newToken:string) {
  token.value = newToken;
  localstorage.set('token', newToken);
}

function removeToken() {
  token.value = null;
  localstorage.remove('token');
}

export { token, setToken, removeToken };
