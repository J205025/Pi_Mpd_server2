<template>
  <!-- Modal Overlay -->
  <Transition name="modal">
    <div 
      v-if="show" 
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeModal"
    >
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>
      
      <!-- Modal content -->
      <div class="flex min-h-screen items-center justify-center p-4">
        <div 
          class="relative bg-white rounded-lg shadow-xl w-full max-w-md p-8 transform transition-all"
          @click.stop
        >
          <!-- Close button -->
          <button
            @click="closeModal"
            class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>

          <h2 class="text-3xl font-extrabold text-gray-900 mb-6 text-center">Change Password</h2>
          
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
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close']);

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

// Reset form when modal is closed
watch(() => props.show, (newVal) => {
  if (!newVal) {
    resetForm();
  }
});

const resetForm = () => {
  form.current_password = '';
  form.new_password = '';
  form.retype_password = '';
  errors.value = {};
  successMessage.value = '';
  isLoading.value = false;
};

const closeModal = () => {
  emit('close');
};

// Validation function
const validateForm = () => {
  const newErrors = {};

  if (!form.current_password) {
    newErrors.current_password = 'Current password is required';
  }

  if (!form.new_password) {
    newErrors.new_password = 'New password is required';
  } else if (form.new_password.length < 6) {
    newErrors.new_password = 'Password must be at least 6 characters long';
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
      setTimeout(() => {
        closeModal();
      }, 2000);
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
/* Modal transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.9);
}
</style>