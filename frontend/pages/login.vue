<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal min-h-screen">
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 flex items-center justify-center">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-6 text-center">Welcome Back</h1>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Name
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.name }"
              placeholder="Enter your name"
            />
            <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.password }"
              placeholder="Enter your password"
            />
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
          </div>

          <div class="flex items-center">
            <input
              id="remember"
              v-model="form.remember"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-700">
              Remember me
            </label>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-full transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Signing In...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <div v-if="errors.general" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {{ errors.general }}
        </div>

        <div v-if="successMessage" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {{ successMessage }}
        </div>

        <div class="mt-6 text-center space-y-2">
          <div>
            <a href="#" class="text-blue-500 hover:text-blue-700 text-sm">Forgot your password?</a>
          </div>
          <div>
            <p class="text-gray-600 text-sm">
              Don't have an account?
              <a href="/register" class="text-blue-500 hover:text-blue-700 font-medium">Sign up here</a>
            </p>
          </div>
        </div>
      </div>
    </main>

    <footer />
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Form data
const form = reactive({
  name: '',
  password: '',
  remember: false
});

watch(() => form.name, (newName) => {
  if (newName && newName.length > 0) {
    const capitalized = newName.charAt(0).toUpperCase() + newName.slice(1);
    if (form.name !== capitalized) {
      form.name = capitalized;
    }
  }
});

// Form state
const errors = ref({});
const isLoading = ref(false);
const successMessage = ref('');

// Validation function
const validateForm = () => {
  const newErrors = {};

  // Name validation
  if (!form.name.trim()) {
    newErrors.name = 'Name is required';
  }

  // Password validation
  if (!form.password) {
    newErrors.password = 'Password is required';
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Handle form submission
const handleLogin = async () => {
  // Clear previous messages
  successMessage.value = '';
  errors.value = {};

  // Validate form
  if (!validateForm()) {
    return;
  }

  isLoading.value = true;

  try {
    // Create FormData for OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append('username', form.name);
    formData.append('password', form.password);

    // Call your FastAPI backend token endpoint
    const response = await fetch(`${apiBase}/token`, {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      
      const token = data.access_token;
      
      // Store token in localStorage to persist it
      localStorage.setItem('authToken', token);
      
      successMessage.value = 'Login successful! Redirecting...';
      
      // Redirect to main page after successful login
      setTimeout(() => {
        window.location.href = '/pcplayer';
      }, 1500);
      
    } else {
      const errorData = await response.json();
      if (response.status === 401) {
        errors.value = { general: 'Invalid name or password. Please try again.' };
      } else {
        errors.value = { general: errorData.detail || 'Login failed. Please try again.' };
      }
    }
    
  } catch (error) {
    console.error('Login error:', error);
    errors.value = { general: 'Network error. Please check your connection and try again.' };
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Additional component-specific styles can be added here */
</style>