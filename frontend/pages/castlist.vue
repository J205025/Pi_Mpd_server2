<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal min-h-screen dark:bg-gray-900">
    <navbar />
    <main class="container mx-auto mt-10 mb-10 p-6 flex flex-col items-center justify-center">
      <h1 class="text-4xl font-bold mb-8 text-gray-800 dark:text-white">Podcast</h1>
      <ul class="space-y-4">
        <li>
          <a href="https://music.j205025.org/podcast/https%3A%2F%2Ffeeds.simplecast.com%2F54nAGcIl" target="_blank" class="text-lg text-blue-500 hover:underline">The Daily</a>
        </li>
        <li>
          <a href="https://music.j205025.org/podcast/https%3A%2F%2Faccess.acast.com%2Frss%2Fec380acc-fe13-46a0-991f-a1e508d126f8" target="_blank" class="text-lg text-blue-500 hover:underline">Economist</a>
        </li>
        <li>
          <a href="https://music.j205025.org/podcast/https%3A%2F%2Ffeeds.megaphone.fm%2FWMHY2007701094" target="_blank" class="text-lg text-blue-500 hover:underline">CNN 5 Things</a>
        </li>
        <li>
          <a href="https://music.j205025.org/podcast/https%3A%2F%2Fpodcastfeeds.nbcnews.com%2Fnbc-meet-the-press" target="_blank" class="text-lg text-blue-500 hover:underline">Meet the Press</a>
        </li>
      </ul>
    </main>
    <footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import navbar from '~/components/navbar.vue';
import footer from '~/components/footer.vue';

const router = useRouter();

onMounted(() => {
  const authToken = localStorage.getItem('authToken');
  if (!authToken) {
    router.push('/login');
  }
});
</script>

<style scoped>
/* Additional component-specific styles can be added here */
</style>
