<script setup lang="ts">

import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const DEFAULT_PHOTO_URL = 'https://api.dicebear.com/6.x/lorelei/svg?seed='

const user = ref({
  username: '',
  name: '',
  about: '',
  joined: '',
  photoURL: '',
});

const usernameInput = ref('');
const nameInput = ref('');
const aboutInput = ref('');
const photoInput = ref(null as File | null);
const photoInputURL = ref('');
const photoURLPREFIX = apiClient.defaults.baseURL + '/'

const errorMessage = ref('');
const successMessage = ref('');

const editProfile = () => {
    errorMessage.value = '';
    successMessage.value = '';
    if(!usernameInput.value || !nameInput.value || !aboutInput.value) {
        errorMessage.value = 'Please fill in all fields.';
        return;
    }
    apiClient.put('/user/0', {
        username: usernameInput.value,
        name: nameInput.value,
        about: aboutInput.value,
        photoURL: user.value.photoURL,
    })
    .then(res => {
        user.value = res.data;
        errorMessage.value = '';
        successMessage.value = 'Profile updated successfully.';
    })
    .catch(err => {
        errorMessage.value = err.response.data.message;
    });
}

const getProfile = () => {
    apiClient.get('/user/0')
    .then(res => {
        user.value = res.data;
        usernameInput.value = user.value.username;
        nameInput.value = user.value.name;
        aboutInput.value = user.value.about;
    })
    .catch(err => {
        if (err.response.status == 401) {
            alert('You are not authorized to access this page. Please login again.');
            router.push('/login');
        }
    });
}

const photoMessageSuccess = ref('');
const photoMessageError = ref('');

const onPhotoSelected = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files) {
        photoInput.value = target.files[0];
    }
    else {
        photoInput.value = null;
    }
}

const photoUpload = () => {
    if (!photoInput.value) {
        photoMessageError.value = 'Please select a photo to upload.';
        return;
    }
    photoMessageError.value = '';
    photoMessageSuccess.value = '';
    const formData = new FormData();
    formData.append('photo', photoInput.value);
    apiClient.post('/photo', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    }).then(res => {
        photoInputURL.value = res.data.path;
        apiClient.put('/user/0', {
            username: user.value.username,
            name: user.value.name,
            about: user.value.about,
            photoURL: photoInputURL.value,
        }).then(res => {
            user.value = res.data;
            photoMessageError.value = '';
            photoMessageSuccess.value = 'Profile photo uploaded successfully.';
        });
    })
    .catch(err => {
        photoMessageError.value = err.response.data.message;
    });
}

const removePhoto = () => {
    photoInputURL.value = '';
    photoMessageError.value = '';
    photoMessageSuccess.value = '';
    apiClient.put('/user/0', {
        username: user.value.username,
        name: user.value.name,
        about: user.value.about,
        photoURL: photoInputURL.value,
    }).then(res => {
        user.value = res.data;
        photoMessageError.value = '';
        photoMessageSuccess.value = 'Profile photo cleared.';
    });
}

const changePasswordMsgError = ref('');
const changePasswordMsgSuccess = ref('');
const newPasswordInput = ref('');
const newPasswordConfirmInput = ref('');

const changePassword = () => {
    changePasswordMsgError.value = '';
    changePasswordMsgSuccess.value = '';
    if (!newPasswordInput.value || !newPasswordConfirmInput.value) {
        changePasswordMsgError.value = 'Please fill in all fields.';
        return;
    }
    if (newPasswordInput.value !== newPasswordConfirmInput.value) {
        changePasswordMsgError.value = 'Passwords do not match.';
        return;
    }
    apiClient.put('/user/0', {
        username: user.value.username,
        name: user.value.name,
        about: user.value.about,
        photoURL: user.value.photoURL,
        password: newPasswordInput.value,
    })
    .then(() => {
        changePasswordMsgError.value = '';
        changePasswordMsgSuccess.value = 'Password changed successfully.';
    })
    .catch(err => {
        changePasswordMsgError.value = err.response.data.message;
    });
}

onMounted(() => {
    getProfile();
});
</script>

<template>
  <div class="profile-view">
    <h1>Profile</h1>
    <div class="profile-body d-flex flex-row align-items-center justify-content-center">
        <div class="profile-photo me-5" >
          <img :src="photoURLPREFIX + user.photoURL" v-if="user.photoURL" />
          <img :src="DEFAULT_PHOTO_URL + user.username" alt="profile-photo" v-else>
        </div>
        <div class="name">
            <h2><strong>{{ user.name }}</strong> (@{{ user.username }})</h2>
        </div>
    </div>
    <p class="mt-3 text-center">{{ user.about }}</p>
    <h1>Edit Profile</h1>
    <form class="editform">
        <div class="input-group mb-3">
            <span class="input-group-text">username:</span>
            <input type="text" class="form-control" v-model="usernameInput" />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text">name:</span>
            <input type="text" class="form-control" v-model="nameInput" />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text">about:</span>
            <input type="text" class="form-control" v-model="aboutInput" />
        </div>
        <div class="successmessage text-success">
            <p>{{ successMessage }}</p>
        </div>
        <div class="errormessage text-danger">
            <p>{{ errorMessage }}</p>
        </div>
        <button type="button" class="btn btn-primary" @click="editProfile">Change Profile</button>
    </form>
    <h1>Change Image</h1>
    <form action="" class="changeimage">
        <div class="input-group mb-3">
            <span class="input-group-text">photo:</span>
            <input type="file" class="form-control" @change="onPhotoSelected" />
            <button @click.prevent="removePhoto" class="btn btn-outline-danger">Clear</button>
        </div>
        <div class="message-error text-danger">
            <p>{{ photoMessageError }}</p>
        </div>
        <div class="message-success text-success">
            <p>{{ photoMessageSuccess }}</p>
        </div>
        <button @click.prevent="photoUpload" class="btn btn-outline-primary">Upload</button>
    </form>
    <h1>Change Password</h1>
    <form action="" class="change-password">
        <div class="input-group mb-3">
            <span class="input-group-text">new password:</span>
            <input required type="password" class="form-control" v-model="newPasswordInput" />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text">confirm password:</span>
            <input required type="password" class="form-control" v-model="newPasswordConfirmInput" />
        </div>
        <div class="successmessage text-success">
            <p>{{ changePasswordMsgSuccess }}</p>
        </div>
        <div class="errormessage text-danger">
            <p>{{ changePasswordMsgError }}</p>
        </div>
        <button @click.prevent="changePassword" type="button" class="btn btn-primary">Change Password</button>
    </form>
  </div>
</template>

<style scoped lang="scss">
.profile-photo{
    width: 150px;
    img{
        width: 150px;
        aspect-ratio: 1/1;
        object-fit: cover;
        border-radius: 50%;
        border: 1px solid black;
    }
}
</style>