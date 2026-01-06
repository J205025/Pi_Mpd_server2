<template>
  <nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex justify-between items-center">
      <NuxtLink :to="'/'" class="text-white text-2xl font-bold">
        My Media Player
      </NuxtLink>
      
      <div class="hidden md:flex items-center space-x-6">
        
        <div class="relative">
          <button @click="togglePcDropdown" class="text-gray-300 hover:text-white transition duration-300 flex items-center">
            電腦播放
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div v-if="isPcDropdownOpen" @mouseleave="closeDropdowns" class="absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-gray-700 z-10">
            <NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="block px-4 py-2 text-gray-300 hover:bg-gray-600 hover:text-white transition duration-300" @click="closeDropdowns">電腦播放</NuxtLink>
            <NuxtLink :to="isLoggedIn ? '/pc_playlist' : '/'" class="block px-4 py-2 text-gray-300 hover:bg-gray-600 hover:text-white transition duration-300" @click="closeDropdowns">電腦歌單</NuxtLink>
          </div>
        </div>

        <div class="relative">
          <button @click="togglePiDropdown" class="text-gray-300 hover:text-white transition duration-300 flex items-center">
            音響播放
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div v-if="isPiDropdownOpen" @mouseleave="closeDropdowns" class="absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-gray-700 z-10">
            <NuxtLink :to="isLoggedIn ? '/piplayer' : '/'" class="block px-4 py-2 text-gray-300 hover:bg-gray-600 hover:text-white transition duration-300" @click="closeDropdowns">音響播放</NuxtLink>
            <NuxtLink :to="isLoggedIn ? '/pi_playlist' : '/'" class="block px-4 py-2 text-gray-300 hover:bg-gray-600 hover:text-white transition duration-300" @click="closeDropdowns">音響歌單</NuxtLink>
          </div>
        </div>
        
        <div class="flex-grow"></div>

        <template v-if="isLoggedIn">
          <NuxtLink to="/userinfo" class="text-gray-300 hover:text-white transition duration-300">Hi, {{ currentUser.toUpperCase() }}</NuxtLink>
          <button @click="handleLogout" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Logout
          </button>
        </template>
      </div>
      
      <button @click="toggleMobileMenu" class="md:hidden text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
        </svg>
      </button>
    </div>
    
    <div :class="{ 'hidden': !isMobileMenuOpen }" class="md:hidden mt-4">
      <NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">電腦播放</NuxtLink>
      <NuxtLink :to="isLoggedIn ? '/pc_playlist' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">電腦歌單</NuxtLink> 
      <NuxtLink :to="isLoggedIn ? '/piplayer' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">音響播放</NuxtLink>
      <NuxtLink :to="isLoggedIn ? '/pi_playlist' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">音響歌單</NuxtLink>      
      <template v-if="isLoggedIn">
        <NuxtLink to="/userinfo" class="block text-gray-300 hover:text-white py-2 px-4">Welcome, {{ currentUser.toUpperCase() }}</NuxtLink>
        <button @click="handleLogout" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Logout
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Mobile menu state
const isMobileMenuOpen = ref(false);
// New state for dropdowns
const isPcDropdownOpen = ref(false);
const isPiDropdownOpen = ref(false);

// Authentication state
const isLoggedIn = ref(false);
const currentUser = ref('');

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// New functions to toggle dropdowns
const closeDropdowns = () => {
  isPcDropdownOpen.value = false;
  isPiDropdownOpen.value = false;
}

const togglePcDropdown = () => {
  isPcDropdownOpen.value = !isPcDropdownOpen.value;
  // Close the other dropdown when this one opens
  isPiDropdownOpen.value = false;
};

const togglePiDropdown = () => {
  isPiDropdownOpen.value = !isPiDropdownOpen.value;
  // Close the other dropdown when this one opens
  isPcDropdownOpen.value = false;
};


// Check authentication status
const checkAuthStatus = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      isLoggedIn.value = false;
      return;
    }

    const response = await fetch(`${apiBase}/users/me/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const userData = await response.json();
      isLoggedIn.value = true;
      currentUser.value = userData.username;
    } else {
      localStorage.removeItem('authToken');
      isLoggedIn.value = false;
      currentUser.value = '';
    }
  } catch (error) {
    console.error('Auth check error:', error);
    isLoggedIn.value = false;
    currentUser.value = '';
  }
};

// Handle logout
const handleLogout = () => {
  localStorage.removeItem('authToken');
  isLoggedIn.value = false;
  currentUser.value = '';
  // Use Nuxt's navigateTo for proper SPA navigation
  navigateTo('/');
};

// Check auth status when component mounts
onMounted(() => {
  checkAuthStatus();
});
</script>