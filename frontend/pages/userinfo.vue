'''<template>
  <div>
    <navbar />
    <main class="container mx-auto mt-4 mb-4 p-6 min-h-screen">
      <div class="bg-white p-6 rounded-lg shadow-xl">

        <div class="flex items-center space-x-6">

          <div class="relative flex-shrink-0">
            <img :src="pictureUrl" @error="onImageError" alt="User Picture" class="w-32 h-32 rounded-full object-cover">
            <label for="pictureUpload" class="absolute bottom-0 right-0 bg-blue-500 text-white p-2 rounded-full cursor-pointer hover:bg-blue-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            </label>
            <input id="pictureUpload" type="file" @change="onFileChange" class="hidden">
          </div>
          <div>
            <h2 class="text-2xl font-semibold">Hi, {{ user.username }}</h2>
          </div>

        </div>
        <div v-if="selectedFile" class="mt-6">
          <img :src="previewUrl" alt="New Picture Preview" class="w-48 h-48 rounded-lg object-cover">
          <button @click="uploadPicture" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Save Picture</button>
        </div>

      </div>


      <div class="bg-white p-6 rounded-lg shadow-xl mt-6">
        <h3 class="text-xl font-semibold mb-4">Settings:</h3>
        <div class="space-y-4">
          <div class="flex items-center">
            <input type="checkbox" id="showLyrics" v-model="settings.show_lyrics" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="showLyrics" class="ml-2 block text-sm text-gray-900">顯示歌詞</label>
          </div>
          <div class="flex items-center">
            <input type="checkbox" id="showRadioCard" v-model="settings.show_radio_card" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="showRadioCard" class="ml-2 block text-sm text-gray-900">顯示廣播頻道</label>
          </div>
          <div class="flex items-center">
            <input type="checkbox" id="id3tagDisplaytype" v-model="settings.id3tagDisplaytype" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="id3tagDisplaytype" class="ml-2 block text-sm text-gray-900">切換ID3tags資訊</label>
          </div>
          <div class="flex items-center">
            <input type="checkbox" id="spareSetting2" v-model="settings.spare_setting2" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="spareSetting1" class="ml-2 block text-sm text-gray-900">Spare Setting 1</label>
          </div>
          <div class="flex items-center">
            <input type="checkbox" id="spareSetting1" v-model="settings.spare_setting1" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="spareSetting2" class="ml-2 block text-sm text-gray-900">Spare Setting 2</label>
          </div>
            <div class="flex items-center">
            <label for="sleepingTime" class="block text-sm text-gray-890">-- Default Sleeping Time(Min): </label>
            <input type="number" id="sleepingTime" v-model.number="settings.sleeping_time" class="ml-2 block w-24 text-sm text-blue-500 border-blue-500 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
          </div>

        </div>
        <div class="mt-6">
          <button @click="saveSettings" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Save Settings</button>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-xl mt-3">
        <div class="mt-2">
          <button 
            @click="showPasswordModal = true"
            class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-6 rounded-lg transition duration-300"
          >
            修改密碼
          </button>
        </div> 
      </div>


    </main>
    <footer />

    <PasswordChangeModal 
      :show="showPasswordModal" 
      @close="showPasswordModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import PasswordChangeModal from '~/components/PasswordChangeModal.vue';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const user = ref({ username: '' });
const settings = ref({
  show_lyrics: true,
  show_radio_card: true,
  sleeping_time: 20,
  spare_setting1: true,
  spare_setting2: true
});
const selectedFile = ref(null);
const previewUrl = ref('');
const cacheBuster = ref('');
const showPasswordModal = ref(false);

const pictureUrl = computed(() => {
  if (user.value.username) {
    const url = `${apiBase}/images/user_picture/${user.value.username}.jpg`;
    return cacheBuster.value ? `${url}?t=${cacheBuster.value}` : url;
  }
  return `${apiBase}/images/user_picture/default.jpg`;
});

onMounted(async () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    window.location.href = '/login';
    return;
  }

  try {
    const response = await $fetch(`${apiBase}/users/me/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    user.value = response;
    if (response.settings) {
      settings.value = response.settings;
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
});

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    previewUrl.value = URL.createObjectURL(file);
  }
};

const onImageError = (event) => {
  event.target.src = `${apiBase}/images/user_picture/default.jpg`;
};

const uploadPicture = async () => {
  if (!selectedFile.value) return;

  const token = localStorage.getItem('authToken');
  if (!token) return;

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    await $fetch(`${apiBase}/upload_user_picture`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    cacheBuster.value = new Date().getTime();
    selectedFile.value = null;
    previewUrl.value = '';
    alert('Picture updated successfully!');
  } catch (error) {
    console.error('Error uploading picture:', error);
    alert('Error uploading picture.');
  }
};

const saveSettings = async () => {
  const token = localStorage.getItem('authToken');
  if (!token) return;

  try {
    await $fetch(`${apiBase}/users/me/settings`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: settings.value
    });
    alert('Settings updated successfully!');
  } catch (error) {
    console.error('Error updating settings:', error);
    alert('Error updating settings.');
  }
};
</script>

<style scoped>
/* Add any additional styling here */
</style>
''