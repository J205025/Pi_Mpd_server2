<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal min-h-screen">


    <main class="container mx-auto mt-10 mb-10 p-6 flex items-center justify-center">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-6 text-center">Change Password</h1>
        
        <form @submit.prevent="handleChangePassword" class="space-y-6">
          <div>
            <label for="current_password" class="block text-sm font-medium text-gray-700 mb-2">
              Current Password
            </label>
            <input
              id="current_password"
              v-model="form.current_password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.current_password }"
              placeholder="Enter your current password"
            />
            <p v-if="errors.current_password" class="mt-1 text-sm text-red-600">{{ errors.current_password }}</p>
          </div>

          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-700 mb-2">
              New Password
            </label>
            <input
              id="new_password"
              v-model="form.new_password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.new_password }"
              placeholder="Enter your new password"
            />
            <p v-if="errors.new_password" class="mt-1 text-sm text-red-600">{{ errors.new_password }}</p>
          </div>

          <div>
            <label for="retype_password" class="block text-sm font-medium text-gray-700 mb-2">
              Re-type New Password
            </label>
            <input
              id="retype_password"
              v-model="form.retype_password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.retype_password }"
              placeholder="Re-type your new password"
            />
            <p v-if="errors.retype_password" class="mt-1 text-sm text-red-600">{{ errors.retype_password }}</p>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-full transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Changing Password...</span>
            <span v-else>Change Password</span>
          </button>
        </form>

        <div v-if="errors.general" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {{ errors.general }}
        </div>

        <div v-if="successMessage" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {{ successMessage }}
        </div>
      </div>
    </main>


  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Form data
const form = reactive({
  current_password: '',
  new_password: '',
  retype_password: ''
});

// Form state
const errors = ref({});
const isLoading = ref(false);
const successMessage = ref('');

// Validation function
const validateForm = () => {
  const newErrors = {};

  if (!form.current_password) {
    newErrors.current_password = 'Current password is required';
  }

  if (!form.new_password) {
    newErrors.new_password = 'New password is required';
  } else if (form.new_password.length < 6) {
    newErrors.new_password = 'Password must be at least 8 characters long';
  }

  if (form.new_password !== form.retype_password) {
    newErrors.retype_password = 'Passwords do not match';
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Handle form submission
const handleChangePassword = async () => {
  successMessage.value = '';
  errors.value = {};

  if (!validateForm()) {
    return;
  }

  isLoading.value = true;

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      errors.value = { general: 'You are not logged in.' };
      return;
    }

    const response = await fetch(`${apiBase}/users/password`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_password: form.current_password,
        new_password: form.new_password
      })
    });

    if (response.ok) {
      successMessage.value = 'Password changed successfully!';
      form.current_password = '';
      form.new_password = '';
      form.retype_password = '';
    } else {
      const errorData = await response.json();
      if (response.status === 400) {
        errors.value = { general: errorData.detail };
      } else {
        errors.value = { general: 'Failed to change password. Please try again.' };
      }
    }
  } catch (error) {
    console.error('Password change error:', error);
    errors.value = { general: 'Network error. Please check your connection and try again.' };
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Additional component-specific styles can be added here */
</style>