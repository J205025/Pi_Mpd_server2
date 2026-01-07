<template>
  <div class="container mx-auto p-4">
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
            <audio controls class="w-full">
              <source :src="episode.audio_url" :type="episode.audio_type || 'audio/mpeg'" />
              Your browser does not support the audio element.
            </audio>
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
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref, watch } from 'vue';
import { useRuntimeConfig } from '#app';

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

const route = useRoute();
const podcastData = ref<PodcastData | null>(null);
const pending = ref(true);
const error = ref<Error | null>(null);
const config = useRuntimeConfig();

const fetchPodcast = async (feedUrl: string) => {
  pending.value = true;
  error.value = null;
  podcastData.value = null;

  try {
    // Decode the URL parameter to get the actual feed URL
    const decodedFeedUrl = decodeURIComponent(feedUrl);
    const response = await fetch(`${config.public.apiBase}/api/podcast_feed?feed_url=${encodeURIComponent(decodedFeedUrl)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (data && data.episodes) {
      data.episodes = data.episodes.slice(0, 10);
    }
    podcastData.value = data;
  } catch (err: any) {
    error.value = err;
  } finally {
    pending.value = false;
  }
};

// Watch for changes in the feedUrl parameter
watch(() => route.params.feedUrl, (newFeedUrl) => {
  if (newFeedUrl) {
    fetchPodcast(newFeedUrl as string);
  }
}, { immediate: true });

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
