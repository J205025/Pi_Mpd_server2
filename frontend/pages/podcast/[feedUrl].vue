<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal min-h-screen dark:bg-gray-900">
    <navbar />
    <main class="container mx-auto p-4">
      <!-- Notification -->
      <div v-if="notification.message" :class="['fixed top-20 right-5 p-4 rounded-lg shadow-md z-50', notification.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white']">
        {{ notification.message }}
      </div>

      <div v-if="pending" class="text-center text-gray-500">Loading podcast...</div>
      <div v-else-if="error" class="text-center text-red-500">Error loading podcast: {{ error.message }}</div>
      <div v-else-if="podcastData && podcastData.feed_info">
        <div class="mb-8 text-center">
          <img
            v-if="podcastData.feed_info.image"
            :src="podcastData.feed_info.image"
            :alt="podcastData.feed_info.title"
            class="mx-auto h-48 w-48 object-cover rounded-lg shadow-md mb-4"
          />
          <h1 class="text-4xl font-bold text-gray-800 mb-2">{{ podcastData.feed_info.title }}</h1>
          <p class="text-lg text-gray-600 mb-4">{{ podcastData.feed_info.description }}</p>
          <a
            v-if="podcastData.feed_info.link"
            :href="podcastData.feed_info.link"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:underline"
          >
            Visit Podcast Website
          </a>
        </div>

        <h2 class="text-3xl font-bold text-gray-800 mb-6 border-b pb-2">Episodes</h2>
        <div class="space-y-6">
          <div
            v-for="episode in podcastData.episodes"
            :key="episode.id"
            class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
          >
            <h3 class="text-2xl font-semibold text-gray-700 mb-2">{{ episode.title }}</h3>
            <p class="text-gray-500 text-sm mb-3">Published: {{ formatDate(episode.published) }}</p>
            <div v-if="episode.summary" class="text-gray-700 mb-4" v-html="episode.summary"></div>
            <div v-else-if="episode.description" class="text-gray-700 mb-4" v-html="episode.description"></div>

            <div v-if="episode.image" class="mb-4">
              <img :src="episode.image" :alt="episode.title" class="max-w-xs h-auto rounded-md shadow-sm" />
            </div>

            <div v-if="episode.audio_url" class="mb-4">
              <audio controls preload="none" class="w-full">
                <source :src="episode.audio_url" :type="episode.audio_type || 'audio/mpeg'" />
                Your browser does not support the audio element.
              </audio>
              <button @click="playOnPi(episode)" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Play on Pi
              </button>
            </div>

            <div class="flex items-center space-x-4 text-gray-600">
              <span v-if="episode.duration">Duration: {{ formatDuration(episode.duration) }}</span>
              <a
                v-if="episode.link"
                :href="episode.link"
                target="_blank"
                rel="noopener noreferrer"
                class="text-blue-500 hover:underline"
              >
                Show Notes
              </a>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-gray-500">No podcast data available.</div>
    </main>
    <footer />
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { ref, watch, onMounted } from 'vue';
import { useRuntimeConfig, useAsyncData } from '#app';
import navbar from '~/components/navbar.vue';
import footer from '~/components/footer.vue';

interface Episode {
  id: string;
  title: string;
  published: string;
  link: string;
  description: string;
  summary: string;
  image: string;
  audio_url: string;
  audio_length: string;
  audio_type: string;
  duration: string;
}

interface FeedInfo {
  title: string;
  link: string;
  description: string;
  image: string;
}

interface PodcastData {
  feed_info: FeedInfo;
  episodes: Episode[];
}

interface Notification {
  message: string;
  type: 'success' | 'error';
}

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();
const notification = ref<Notification>({ message: '', type: 'success' });

onMounted(() => {
  const authToken = localStorage.getItem('authToken');
  if (!authToken) {
    router.push('/login');
  }
});

const showNotification = (message: string, type: 'success' | 'error' = 'success', duration: number = 3000) => {
  notification.value = { message, type };
  setTimeout(() => {
    notification.value.message = '';
  }, duration);
};

const playOnPi = async (episode: Episode) => {
  const authToken = localStorage.getItem('authToken');
  if (!authToken) {
    showNotification('You must be logged in to perform this action.', 'error');
    return;
  }

  try {
    const response = await fetch(`${config.public.apiBase}/pi_add_and_play_stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        stream_url: episode.audio_url,
        title: episode.title,
        artist: podcastData.value?.feed_info.title || 'Podcast',
      }),
    });

    if (response.ok) {
      const result = await response.json();
      showNotification(result.message || 'Started playing on Pi.', 'success');
    } else {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to play on Pi.');
    }
  } catch (error) {
    console.error('Error playing on Pi:', error);
    showNotification(error.message || 'An unexpected error occurred.', 'error');
  }
};


const { data: podcastData, pending, error } = await useAsyncData<PodcastData>(
  'podcast',
  async () => {
    const feedUrl = route.params.feedUrl as string;
    if (!feedUrl) {
      return null;
    }
    const decodedFeedUrl = decodeURIComponent(feedUrl);
    const response = await fetch(`${config.public.apiBase}/api/podcast_feed?feed_url=${encodeURIComponent(decodedFeedUrl)}&limit=3`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },
  {
    watch: [() => route.params.feedUrl]
  }
);


const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A';
  try {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return dateString; // Return original if parsing fails
  }
};

const formatDuration = (durationString: string) => {
  if (!durationString) return 'N/A';
  // Duration can be in 'HH:MM:SS' or 'MM:SS' or seconds
  const parts = durationString.split(':').map(Number);
  if (parts.length === 3) {
    return `${parts[0]}h ${parts[1]}m ${parts[2]}s`;
  } else if (parts.length === 2) {
    return `${parts[0]}m ${parts[1]}s`;
  } else {
    const totalSeconds = parseInt(durationString, 10);
    if (!isNaN(totalSeconds)) {
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      let formatted = '';
      if (hours > 0) formatted += `${hours}h `;
      if (minutes > 0 || hours > 0) formatted += `${minutes}m `;
      formatted += `${seconds}s`;
      return formatted.trim();
    }
  }
  return durationString;
};
</script>

<style scoped>
/* Add any specific styles here if needed */
</style>
