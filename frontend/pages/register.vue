<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal min-h-screen">
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 flex items-center justify-center">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-6 text-center">Create Account</h1>
        
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.name }"
              placeholder="Enter your full name"
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

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.confirmPassword }"
              placeholder="Confirm your password"
            />
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">{{ errors.confirmPassword }}</p>
          </div>

          <div>
            <label for="registrationCode" class="block text-sm font-medium text-gray-700 mb-2">
              Registration Code
            </label>
            <input
              id="registrationCode"
              v-model="form.code"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.code }"
              placeholder="Enter the registration code"
            />
            <p v-if="errors.code" class="mt-1 text-sm text-red-600">{{ errors.code }}</p>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-full transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Creating Account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>

        <div v-if="successMessage" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {{ successMessage }}
        </div>
        
        <div v-if="errors.general" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {{ errors.general }}
        </div>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Already have an account?
            <a href="/login" class="text-blue-500 hover:text-blue-700 font-medium">Sign in here</a>
          </p>
        </div>
      </div>
    </main>

    <footer />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Form data
const form = reactive({
  name: '',
  password: '',
  confirmPassword: '',
  code: '' // <-- Add code field
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
  } else if (form.name.trim().length < 2) {
    newErrors.name = 'Name must be at least 2 characters';
  }

  // Password validation
  if (!form.password) {
    newErrors.password = 'Password is required';
  } else if (form.password.length < 6) {
    newErrors.password = 'Password must be at least 6 characters';
  }

  // Confirm password validation
  if (!form.confirmPassword) {
    newErrors.confirmPassword = 'Please confirm your password';
  } else if (form.password !== form.confirmPassword) {
    newErrors.confirmPassword = 'Passwords do not match';
  }

  // Registration code validation
  if (!form.code.trim()) {
    newErrors.code = 'Registration code is required';
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Handle form submission
const handleRegister = async () => {
  // Clear previous messages
  successMessage.value = '';

  // Validate form
  if (!validateForm()) {
    return;
  }

  isLoading.value = true;

  try {
    // Call your FastAPI backend
    const response = await fetch(`${apiBase}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: form.name,
        password: form.password,
        code: form.code // <-- Send the code
      })
    });

    if (response.ok) {
      const data = await response.json();
      successMessage.value = 'Account created successfully! You can now log in.';
      
      // Reset form
      Object.assign(form, {
        name: '',
        password: '',
        confirmPassword: '',
        code: '' // <-- Reset code field
      });
      
      // Redirect to login after 2 seconds
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
      
    } else {
      const errorData = await response.json();
      // Clear all previous errors before setting new ones
      errors.value = {}; 
      if (response.status === 400) {
          if (errorData.detail === "Username already registered") {
              errors.value = { name: 'Username already exists. Please choose a different name.' };
          } else if (errorData.detail === "Invalid registration code") {
              errors.value = { code: 'The registration code is incorrect.' };
          } else {
              errors.value = { general: errorData.detail || 'Registration failed. Please try again.' };
          }
      } else {
          errors.value = { general: errorData.detail || 'Registration failed. Please try again.' };
      }
    }
    
  } catch (error) {
    console.error('Registration error:', error);
    errors.value = { general: 'Network error. Please check your connection and try again.' };
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Additional component-specific styles can be added here */
</style>