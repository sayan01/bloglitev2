<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { apiClient } from '@/axios';
import type { UserType } from '@/types/UserType';

const user = ref({} as UserType);

onMounted(() => {
    getUser();
});

const getUser = () => {
    apiClient.get('/user')
    .then(res => {
        user.value = res.data;
        usernameInput.value = user.value.username;
        nameInput.value = user.value.name;
        aboutInput.value = user.value.about;
    })
    .catch(err => {
        console.log(err);
    });
}

const usernameInput = ref('');
const nameInput = ref('');
const aboutInput = ref('');
const photoInput = ref(null as File | null);
const photoInputURL = ref('');

const errorMessage = ref('');
const successMessage = ref('');

const editProfile = () => {
    errorMessage.value = '';
    successMessage.value = '';
    if(!usernameInput.value || !nameInput.value || !aboutInput.value) {
        errorMessage.value = 'Please fill in all fields.';
        return;
    }
    apiClient.put('/user', {
        username: usernameInput.value,
        name: nameInput.value,
        about: aboutInput.value,
        photoURL: user.value.photoURL,
    })
    .then(() => {
        errorMessage.value = '';
        successMessage.value = 'Profile updated successfully.';
    })
    .catch(err => {
        errorMessage.value = err.response.data.message;
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
        apiClient.put('/user', {
            username: user.value.username,
            name: user.value.name,
            about: user.value.about,
            photoURL: photoInputURL.value,
        }).then(() => {
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
    apiClient.put('/user', {
        username: user.value.username,
        name: user.value.name,
        about: user.value.about,
        photoURL: photoInputURL.value,
    }).then(() => {
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
    apiClient.put('/user', {
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

</script>

<template>
  <div class="edit-profile-view">
    <div class="profile-edit">
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
    </div>
    <hr>
    <div class="profile-change-image">
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
    </div>
    <hr>
    <div class="profile-change-password">
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
  </div>
</template>

<style scoped lang="scss">
.profile-edit, .profile-change-image, .profile-change-password{
    min-height: 30svh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
</style>