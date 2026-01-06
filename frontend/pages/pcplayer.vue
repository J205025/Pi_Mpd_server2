<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-4 mb-4 p-2 sm:p-4 md:p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl text-center">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900">電腦播放(Pc Player)</h1>
      </div>

      <div  class="bg-white p-6 rounded-lg shadow-xl mt-4">
        <div class="text-center mb-4">
          <p class="text-gray-600 font-bold">{{ trackTitle }}</p>
          <p class="text-gray-500 text-sm mt-1">
            <span v-if="trackArtist">{{ trackArtist }}</span>
            <span v-if="trackArtist && trackAlbum"> - </span>
            <span v-if="trackAlbum">{{ trackAlbum }}</span>
          </p>
        </div>

        <audio 
          ref="audioPlayer"
          @loadedmetadata="onLoadedMetadata"
          @timeupdate="onTimeUpdate"
          @ended="onTrackEnded"
          @loadstart="isLoading = true"
          @canplay="handleCanPlay"
          @error="onAudioError"
          @canplaythrough="onCanPlayThrough"
          preload="metadata"
          class="w-full"
        ></audio>

<div class="mb-6">
    <div v-if="!isPlayingLiveStream">
        <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
        </div>
        <div 
            class="w-full bg-gray-200 rounded-full h-2 cursor-pointer"
            @click="seekTo($event)"
        >
            <div 
                class="bg-blue-600 h-2 rounded-full transition-all duration-100"
                :style="{ width: progressPercentage + '%' }"
            ></div>
        </div>
    </div>

    <div v-else class="text-center py-2">
        <span class="text-red-500 font-bold text-lg animate-pulse">🔴 LIVE</span>
        <p class="text-gray-500 text-sm mt-1">Elapsed: {{ formatTime(currentTime) }}</p>
    </div>
</div>

        <div class="flex items-center justify-center space-x-4 md:space-x-6">
          <button
            @click="previousTrack"
            :disabled="pc_playlist_all.length <= 1"
            class="p-2 rounded-full transition-colors duration-200 bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-5 h-5 md:w-6 md:h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M8.445 14.832A1 1 0 0010 14v-2.798l5.445 3.63A1 1 0 0017 14V6a1 1 0 00-1.555-.832L10 8.798V6a1 1 0 00-1.555-.832l-6 4a1 1 0 000 1.664l6 4z"/>
            </svg>
          </button>

          <button
            @click="togglePlayPause"
            :disabled="isLoading"
            class="w-16 h-16 md:w-24 md:h-24 rounded-full bg-blue-500 hover:bg-blue-600 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed text-white transition-colors duration-200 flex items-center justify-center shadow-lg"
          >
            <svg v-if="isLoading" class="w-8 h-8 md:w-12 md:h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/>
            </svg>
            <svg v-else-if="isPlaying" class="w-8 h-8 md:w-12 md:h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/>
            </svg>
            <svg v-else class="w-8 h-8 md:w-12 md:h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/>
            </svg>
          </button>

          <button
            @click="nextTrack"
            :disabled="pc_playlist_all.length <= 1"
            class="p-2 rounded-full transition-colors duration-200 bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-5 h-5 md:w-6 md:h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z"/>
            </svg>
          </button>

          <!-- Favorite Button -->
          <button @click="pc_toggleFavorite" :disabled="!selectedTrack || selectedTrack === 'LIVE_STREAM'" class="p-2 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed md:p-3">
            <svg v-if="isFavorite" class="w-5 h-5 md:w-6 md:h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="w-5 h-5 md:w-6 md:h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 20 20">
              <path d="M17.5 9.16666C17.5 12.5 14.1667 15.8333 10 17.5C5.83333 15.8333 2.5 12.5 2.5 9.16666C2.5 7.04738 4.21401 5.33333 6.33333 5.33333C7.53594 5.33333 8.6425 5.84196 9.39999 6.69433L10 7.35766L10.6 6.69433C11.3575 5.84196 12.4641 5.33333 13.6667 5.33333C15.786 5.33333 17.5 7.04738 17.5 9.16666Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <div class="flex flex-col md:flex-row items-center justify-between mt-6 space-y-4 md:space-y-0">
          <div class="flex items-center space-x-2">
            <button @click="toggleMute" class="p-2 rounded-full text-gray-600 hover:text-gray-800">
              <svg v-if="isMuted || volume === 0" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.293 7.293a1 1 0 011.414 0L15 8.586l1.293-1.293a1 1 0 111.414 1.414L16.414 10l1.293 1.293a1 1 0 01-1.414 1.414L15 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L13.586 10l-1.293-1.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
              <svg v-else-if="volume < 0.5" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.146 6.146a.5.5 0 01.708 0l.646.647.646-.647a.5.5 0 11.708.708L13.207 8.5l1.647 1.646a.5.5 0 01-.708.708L12.5 9.207l-.646.647a.5.5 0 11-.708-.708L12.793 7.5l-1.647-1.646a.5.5 0 010-.708z" clip-rule="evenodd"></path></svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM15.657 6.343a1 1 0 00-1.414 1.414.5.5 0 000 .707l.707.707a1 1 0 101.414-1.414l-.707-.707a.5.5 0 000-.707zm1.414 5.657a1 1 0 01-1.414 0 .5.5 0 000-.707l-.707-.707a1 1 0 111.414-1.414l.707.707a.5.5 0 000 .707z" clip-rule="evenodd"></path></svg>
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              v-model="volume"
              @input="updateVolume"
              class="w-24 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            >
            <span class="text-sm text-gray-600 w-8">{{ Math.round(volume * 100) }}</span>
          </div>

          <div class="flex items-center space-x-2">
            <button
              @click="togglePlaybackRate"
              class="p-2 rounded w-16 text-center transition-colors duration-200 text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 font-semibold"
              title="Toggle Playback Speed"
            >
              {{ playbackRate.toFixed(2) }}x
            </button>

            <button
              @click="toggleShuffle"
              :class="['p-2 rounded-full transition-colors duration-200', shuffleMode ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800']"
            ><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732L14.146 12.8l-1.179 4.456a1 1 0 01-1.856-.288L12.382 12H10a1 1 0 110-2h2.382l-.271-4.968A1 1 0 0112 2z" clip-rule="evenodd"></path></svg></button>

            <button
              @click="toggleRepeat"
              :class="['p-2 rounded-full transition-colors duration-200', repeatMode === 'none' ? 'text-gray-600 hover:text-gray-800' : 'bg-blue-100 text-blue-600']"
            >
              <svg v-if="repeatMode === 'one'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5.05 4.05a7 7 0 000 9.9 7 7 0 009.9 0a1 1 0 111.414 1.414 9 9 0 01-12.728 0 9 9 0 010-12.728A9 9 0 0110 1.05a1 1 0 110 2 7 7 0 00-4.95 1zM14.95 15.95a7 7 0 000-9.9 7 7 0 00-9.9 0a1 1 0 11-1.414-1.414 9 9 0 0112.728 0 9 9 0 010 12.728A9 9 0 0110 18.95a1 1 0 110-2 7 7 0 004.95-1z"></path></svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 12V7H3l4-4 4 4H9v5a1 1 0 01-1 1H5zm10 1v5h2l-4 4-4-4h2V8a1 1 0 011-1h3z"></path></svg>
            </button>

            <button
              @click="cycleSleepTimer"
              :class="['p-2 rounded w-28 text-center transition-colors duration-200 font-semibold', activeSleepDuration ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200']"
              title="Cycle Sleep Timer"
            >
              <div class="flex items-center justify-center">
                <svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                <span v-if="sleepTimeRemaining !== null">{{ formatTime(sleepTimeRemaining) }}</span>
                <span v-else>Sleep</span>
              </div>
            </button>
          </div>
        </div>

        <div class="mt-4 text-center text-sm text-gray-500">
          Track {{ currentTrackIndex + 1 }} of {{ pc_playlist_all.length }}
          <span v-if="shuffleMode" class="ml-2">(Shuffle)</span>
          <span v-if="repeatMode === 'all'" class="ml-2">(Repeat All)</span>
          <span v-if="repeatMode === 'one'" class="ml-2">(Repeat One)</span>
        </div>
      </div>

      <!-- Lyrics Display Component -->
      <pc_LyricDisplay 
        :trackPath="selectedTrack"
        :currentTime="currentTime"
        :isLiveStream="isPlayingLiveStream"
        :apiBase="apiBase"
      />

      <div class="bg-white p-6 rounded-lg shadow-xl mt-4">
        <label for="load-playlist-select" class="block text-xl font-bold mb-3 text-gray-800">選擇歌單:</label>
        <select
          id="load-playlist-select"
          @change="loadPlaylist($event.target.value)"
          class="block w-full p-3 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        >
          <option disabled selected value="">-- Choose a playlist --</option>
          <option v-for="name in sortedPlaylistNames" :key="name" :value="name" :class="{ 'text-red-600': name === '我的最愛' }">
            {{ name }}
          </option>
        </select>
      </div>

      <div v-if="pc_playlist_all.length > 0" class="bg-white p-6 rounded-lg shadow-xl mt-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-3">播放佇列:</h3>
        <ul class="list-none bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
          <li v-for="(track, index) in pc_playlist_all" :key="index"
              @click="playTrack(track)"
              class="text-gray-700 p-1 truncate cursor-pointer hover:bg-blue-100"
              :class="{ 'bg-blue-200': track === selectedTrack }">
            {{ index + 1 }}. {{ getTrackArtist(track) }} - {{ getTrackAlbum(track) }} - {{ getTrackTitle(track) }}
          </li>
        </ul>
      </div>

      <pc_radiocard 
        :loadingStreamTitle="loadingStreamTitle"
        :isPlayingLiveStream="isPlayingLiveStream"
        :currentStreamInfo="currentStreamInfo"
        @play-stream="handlePlayStream"
      />

    </main>
    
    <footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue';
import pc_LyricDisplay from '~/components/pc_lyricdisplay.vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const pc_playlist_all = ref([]);
const selectedTrack = ref('');
const loading = ref(false);
const error = ref(null);

// State for playlist names
const playlistNames = ref([]);

const sortedPlaylistNames = computed(() => {
  const names = [...playlistNames.value];
  const favorite = '我的最愛';
  
  const favoritePlaylist = names.filter(p => p === favorite);
  const otherPlaylists = names.filter(p => p !== favorite);
  
  return [...favoritePlaylist, ...otherPlaylists];
});

// Audio player state
const audioPlayer = ref(null);
const isPlaying = ref(false);
const isLoading = ref(false);
const currentTime = ref(0);
const duration = ref(0);
const volume = ref(0.7);
const isMuted = ref(false);
const previousVolume = ref(0.7);
const autoPlayOnLoad = ref(true);

// State for playback speed
const playbackRate = ref(1.0);
const availableRates = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5];

// HLS.js instance
let hls = null;

// Play modes
const shuffleMode = ref(false);
const repeatMode = ref('none'); // 'none', 'all', 'one'

// State for stream metadata
const currentStreamInfo = ref(null);
const loadingStreamTitle = ref(null);
let loadingTimer = null;
const LOADING_TIMEOUT = 15000;

// Sleep timer state
const sleepDurations = [5,10, 15, 20, 25, 30, 35, 40, 50, 60];
const activeSleepDuration = ref(null);
const sleepTimeRemaining = ref(null);
const sleepTimerId = ref(null);

// Computed property to check if a live stream is playing
const isPlayingLiveStream = computed(() => {
  return isPlaying.value && selectedTrack.value === 'LIVE_STREAM';
});

const favoritePlaylist = ref([]);
const isFavorite = computed(() => {
  if (!selectedTrack.value || selectedTrack.value === 'LIVE_STREAM' || !favoritePlaylist.value) return false;
  return favoritePlaylist.value.includes(selectedTrack.value);
});


// Computed properties
const currentTrackIndex = computed(() => {
  if (selectedTrack.value === 'LIVE_STREAM') return -1;
  return pc_playlist_all.value.findIndex(track => track === selectedTrack.value);
});

const progressPercentage = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 : 0;
});

// Functions for parsing track metadata
const getTrackTitle = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.pop().replace(/\.(mp3|MP3|flac|FLAC)$/, '');
};

const getTrackAlbum = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.length > 2 ? parts[parts.length - 2] : '';
};

const getTrackArtist = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.length > 2 ? parts[parts.length - 3] : '';
};

// Computed properties for display
const trackTitle = computed(() => {
    if (selectedTrack.value === 'LIVE_STREAM' && currentStreamInfo.value) {
        return currentStreamInfo.value.title;
    }
    return getTrackTitle(selectedTrack.value);
});

const trackAlbum = computed(() => {
    if (selectedTrack.value === 'LIVE_STREAM') {
        return '';
    }
    return getTrackAlbum(selectedTrack.value);
});

const trackArtist = computed(() => {
    if (selectedTrack.value === 'LIVE_STREAM' && currentStreamInfo.value) {
        return currentStreamInfo.value.artist;
    }
    return getTrackArtist(selectedTrack.value);
});

// Helper function to check if URL is an HLS stream
const isHLSStream = (url) => {
  return url.toLowerCase().includes('.m3u8');
};

// Helper function to load HLS.js library
const loadHLS = async () => {
  if (window.Hls) {
    return window.Hls;
  }
  
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/hls.js/1.4.12/hls.min.js';
    script.onload = () => resolve(window.Hls);
    script.onerror = () => reject(new Error('Failed to load HLS.js'));
    document.head.appendChild(script);
  });
};

// Helper function to destroy existing HLS instance
const destroyHLS = () => {
  if (hls) {
    hls.destroy();
    hls = null;
  }
};

// Fetch initial data on component mount
onMounted(async () => {
  loading.value = true;
  error.value = null;

  const token = localStorage.getItem('authToken');
  if (!token) {
    // Redirect to login or show an error
    window.location.href = '/login';
    return;
  }

  try {
    // Fetch the default list of all available files
    const allFilesResponse = await $fetch(`${apiBase}/pc_get_allfiles`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (Array.isArray(allFilesResponse)) {
      pc_playlist_all.value = allFilesResponse;
      console.log('Default track list loaded:', pc_playlist_all.value);
      // If the playlist has tracks, select the first one to display the player.
      if (pc_playlist_all.value.length > 0) {
        selectedTrack.value = pc_playlist_all.value[0];
        autoPlayOnLoad.value = false; // Prevents it from playing automatically
      }      
    } else {
      console.error('Invalid format for all files list:', allFilesResponse);
    }

    // Fetch the list of user-saved playlist names
    const playlistNamesResponse = await $fetch(`${apiBase}/pc_get_playlist_List`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (playlistNamesResponse && Array.isArray(playlistNamesResponse.names)) {
      playlistNames.value = playlistNamesResponse.names;
      console.log('Playlist names received:', playlistNames.value);
    } else {
      console.error('Invalid format for playlist names:', playlistNamesResponse);
    }

    // Fetch the "我的最愛" playlist
    const favPlaylistResponse = await $fetch(`${apiBase}/pc_playlist_files/我的最愛`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (Array.isArray(favPlaylistResponse)) {
      favoritePlaylist.value = favPlaylistResponse;
      console.log('Favorite playlist loaded:', favoritePlaylist.value);
    } else {
      console.error('Invalid format for favorite playlist:', favPlaylistResponse);
    }

  } catch (err) {
    console.error('Error fetching initial data:', err);
    error.value = `Failed to fetch data: ${err.message || 'Unknown error'}`;
  } finally {
    loading.value = false;
  }
});

// Clean up HLS instance and timers on unmount
onBeforeUnmount(() => {
  destroyHLS();
  if (sleepTimerId.value) {
    clearInterval(sleepTimerId.value);
  }
});

// Function to load tracks from a selected playlist
const loadPlaylist = async (playlistName) => {
  if (!playlistName) return;

  console.log(`Loading playlist: ${playlistName}`);
  loading.value = true;
  error.value = null;

  const token = localStorage.getItem('authToken');
  if (!token) {
    // Redirect to login or show an error
    window.location.href = '/login';
    return;
  }

  try {
    const response = await $fetch(`${apiBase}/pc_playlist_files/${playlistName}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (Array.isArray(response)) {
      pc_playlist_all.value = response;
      console.log('Tracks for', playlistName, 'loaded:', pc_playlist_all.value);
      
      if (playlistName === '我的最愛') {
        favoritePlaylist.value = [...response]; // Create a copy
      }

      // Automatically select the first track of the new playlist
      if (pc_playlist_all.value.length > 0) {
        selectedTrack.value = pc_playlist_all.value[0];
        autoPlayOnLoad.value = false; // Optional: auto-play the first track
      } else {
        selectedTrack.value = ''; // Clear selection if playlist is empty
      }
    } else {
      console.error('Invalid response format for playlist files:', response);
      error.value = 'Invalid response format from server';
    }
  } catch (err) {
    console.error(`Error fetching playlist ${playlistName}:`, err);
    error.value = `Failed to fetch playlist: ${err.message || 'Unknown error'}`;
  } finally {
    loading.value = false;
  }
};

// Watch for volume changes
watch(volume, (newVolume) => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = newVolume;
    if (newVolume > 0 && isMuted.value) {
      isMuted.value = false;
    }
  }
});

// Watch for playback rate changes
watch(playbackRate, (newRate) => {
  if (audioPlayer.value) {
    audioPlayer.value.playbackRate = newRate;
  }
});

// Watcher for source control
watch(selectedTrack, (newTrack) => {
  if (!audioPlayer.value) return;
  
  // Destroy any existing HLS instance when switching tracks
  destroyHLS();
  
  // This watcher handles changing the source ONLY for playlist tracks.
  // The live stream source is set manually in its own function.
  if (newTrack && newTrack !== 'LIVE_STREAM') {
    audioPlayer.value.src = `${apiBase}/music/${newTrack}`;
    audioPlayer.value.load(); // Tell the browser to load the new source
  }
});

// Function to play streams with HLS support
const playStream = async (streamUrl, streamTitle, streamArtist) => {
  if (!audioPlayer.value) return;

  // Clear any previous loading timer
  clearTimeout(loadingTimer);
  // Set the title of the stream currently attempting to load
  loadingStreamTitle.value = streamTitle;

  if (isPlaying.value) {
    audioPlayer.value.pause();
    isPlaying.value = false;
  }
  
  // Destroy any existing HLS instance
  destroyHLS();
  
  // Start a timer to stop loading and hide the icon if playback doesn't begin
  loadingTimer = setTimeout(() => {
    if (!isPlaying.value || selectedTrack.value !== 'LIVE_STREAM') {
      console.log('Stream loading timed out. Stopping playback attempt.');
      audioPlayer.value.pause();
      audioPlayer.value.src = '';
      destroyHLS();
      loadingStreamTitle.value = null; // Hide the icon
    }
  }, LOADING_TIMEOUT);

  // Set stream info
  selectedTrack.value = 'LIVE_STREAM';
  currentStreamInfo.value = {
    title: streamTitle,
    artist: streamArtist
  };

  try {
    if (isHLSStream(streamUrl)) {
      // Handle HLS streams (.m3u8)
      console.log('Loading HLS stream:', streamUrl);
      
      // Load HLS.js library if not already loaded
      const Hls = await loadHLS();
      
      if (Hls.isSupported()) {
        hls = new Hls({
          enableWorker: true,
          lowLatencyMode: true,
          backBufferLength: 90
        });
        
        hls.loadSource(streamUrl);
        hls.attachMedia(audioPlayer.value);
        
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          console.log('HLS manifest parsed successfully');
          audioPlayer.value.play().then(() => {
            isPlaying.value = true;
            clearTimeout(loadingTimer);
            loadingStreamTitle.value = null;
          }).catch(error => {
            console.error('Error playing HLS stream:', error);
            isPlaying.value = false;
            clearTimeout(loadingTimer);
            loadingStreamTitle.value = null;
            alert(`Failed to play ${streamTitle}. Please try again.`);
          });
        });
        
        hls.on(Hls.Events.ERROR, (event, data) => {
          console.error('HLS error:', data);
          if (data.fatal) {
            switch (data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                console.error('Fatal network error encountered, trying to recover');
                hls.startLoad();
                break;
              case Hls.ErrorTypes.MEDIA_ERROR:
                console.error('Fatal media error encountered, trying to recover');
                hls.recoverMediaError();
                break;
              default:
                console.error('Fatal error, cannot recover');
                destroyHLS();
                isPlaying.value = false;
                clearTimeout(loadingTimer);
                loadingStreamTitle.value = null;
                alert(`HLS stream error for ${streamTitle}. Please try again.`);
                break;
            }
          }
        });
        
      } else if (audioPlayer.value.canPlayType('application/vnd.apple.mpegurl')) {
        // Fallback for browsers with native HLS support (Safari)
        console.log('Using native HLS support');
        audioPlayer.value.src = streamUrl;
        await audioPlayer.value.load();
        await audioPlayer.value.play();
        isPlaying.value = true;
        clearTimeout(loadingTimer);
        loadingStreamTitle.value = null;
      } else {
        throw new Error('HLS is not supported in this browser');
      }
    } else {
      // Handle regular audio streams (MP3, etc.)
      console.log('Loading regular audio stream:', streamUrl);
      audioPlayer.value.src = streamUrl;
      await audioPlayer.value.load();
      await audioPlayer.value.play();
      isPlaying.value = true;
      clearTimeout(loadingTimer);
      loadingStreamTitle.value = null;
    }
  } catch (error) {
    console.error("Error playing stream:", error);
    isPlaying.value = false;
    clearTimeout(loadingTimer);
    loadingStreamTitle.value = null;
    destroyHLS();
    alert(`Failed to connect to ${streamTitle}. The station may be offline or your connection may be blocked.`);
  }
};

// Event handler for the child component's event
const handlePlayStream = (streamData) => {
  playStream(streamData.url, streamData.title, streamData.artist);
};

// Audio player methods
const playTrack = (track) => {
  selectedTrack.value = track;
  autoPlayOnLoad.value = true;
};

const handleCanPlay = () => {
  isLoading.value = false;
  // Clear the timer and loading icon state when playback is ready
  clearTimeout(loadingTimer);
  loadingStreamTitle.value = null; 
  if (autoPlayOnLoad.value) {
    autoPlayOnLoad.value = false;
    audioPlayer.value.play().then(() => {
      isPlaying.value = true;
    }).catch(error => {
      console.error('Autoplay was prevented.', error);
      isPlaying.value = false;
    });
  }
};

const togglePlayPause = () => {
  if (!audioPlayer.value || (!audioPlayer.value.src && !hls)) return;
  if (isPlaying.value) {
    audioPlayer.value.pause();
    isPlaying.value = false;
  } else {
    audioPlayer.value.play().catch((error) => {
      console.error('Error playing audio:', error);
      isPlaying.value = false;
    });
    isPlaying.value = true; // Assume play will succeed
  }
};

const onLoadedMetadata = () => {
  if (audioPlayer.value) {
    // For live streams, duration can be Infinity. Handle this.
    const newDuration = audioPlayer.value.duration;
    duration.value = isFinite(newDuration) ? newDuration : 0;
    audioPlayer.value.volume = volume.value;
    audioPlayer.value.playbackRate = playbackRate.value;
  }
};

const onTimeUpdate = () => {
  if (audioPlayer.value) {
    currentTime.value = audioPlayer.value.currentTime;
  }
};

const onTrackEnded = () => {
  isPlaying.value = false;
  // Do not auto-play next track if it was a stream
  if (selectedTrack.value === 'LIVE_STREAM') return;

  if (repeatMode.value === 'one') {
    audioPlayer.value.currentTime = 0;
    audioPlayer.value.play();
    isPlaying.value = true;
  } else if (repeatMode.value === 'all' || shuffleMode.value) {
    nextTrack(true);
  } else {
    const nextIndex = currentTrackIndex.value + 1;
    if (nextIndex < pc_playlist_all.value.length) {
      nextTrack(true);
    }
  }
};

const seekTo = (event) => {
  // Disable seeking for live streams
  if (!audioPlayer.value || duration.value === 0) return;
  const rect = event.currentTarget.getBoundingClientRect();
  const percentage = (event.clientX - rect.left) / rect.width;
  audioPlayer.value.currentTime = percentage * duration.value;
};

const previousTrack = (shouldPlay = isPlaying.value) => {
  if (pc_playlist_all.value.length <= 1) return;
  
  // Stop any HLS stream when switching to playlist tracks
  destroyHLS();
  
  let newIndex;
  if (shuffleMode.value) {
    do {
      newIndex = Math.floor(Math.random() * pc_playlist_all.value.length);
    } while (newIndex === currentTrackIndex.value && pc_playlist_all.value.length > 1);
  } else {
    newIndex = currentTrackIndex.value - 1;
    if (newIndex < 0) {
      newIndex = repeatMode.value === 'all' ? pc_playlist_all.value.length - 1 : 0;
    }
  }
  selectedTrack.value = pc_playlist_all.value[newIndex];
  autoPlayOnLoad.value = shouldPlay;
};

const nextTrack = (shouldPlay = isPlaying.value) => {
  if (pc_playlist_all.value.length <= 1) return;
  
  // Stop any HLS stream when switching to playlist tracks
  destroyHLS();
  
  let newIndex;
  if (shuffleMode.value) {
    do {
      newIndex = Math.floor(Math.random() * pc_playlist_all.value.length);
    } while (newIndex === currentTrackIndex.value && pc_playlist_all.value.length > 1);
  } else {
    newIndex = currentTrackIndex.value + 1;
    if (newIndex >= pc_playlist_all.value.length) {
      newIndex = repeatMode.value === 'all' ? 0 : pc_playlist_all.value.length - 1;
    }
  }
  selectedTrack.value = pc_playlist_all.value[newIndex];
  autoPlayOnLoad.value = shouldPlay;
};

const updateVolume = () => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value;
  }
};

const toggleMute = () => {
  if (isMuted.value) {
    volume.value = previousVolume.value;
    isMuted.value = false;
  } else {
    previousVolume.value = volume.value;
    volume.value = 0;
    isMuted.value = true;
  }
};

const toggleShuffle = () => {
  shuffleMode.value = !shuffleMode.value;
};

const toggleRepeat = () => {
  const modes = ['none', 'all', 'one'];
  const currentIndex = modes.indexOf(repeatMode.value);
  repeatMode.value = modes[(currentIndex + 1) % modes.length];
};

// Function to toggle playback speed
const togglePlaybackRate = () => {
  const currentIndex = availableRates.indexOf(playbackRate.value);
  const nextIndex = (currentIndex + 1) % availableRates.length;
  playbackRate.value = availableRates[nextIndex];
};

// Sleep timer function
const cycleSleepTimer = () => {
  // 1. Clear any existing interval to reset the timer
  if (sleepTimerId.value) {
    clearInterval(sleepTimerId.value);
    sleepTimerId.value = null;
  }

  // 2. Find the index of the current duration and determine the next one
  let nextIndex;
  if (activeSleepDuration.value === null) {
    // If timer is off, start with the first duration (e.g., 10 minutes)
    nextIndex = 0;
  } else {
    const currentIndex = sleepDurations.indexOf(activeSleepDuration.value);
    nextIndex = currentIndex + 1;
  }

  // 3. If we've cycled past the last duration, turn the timer off
  if (nextIndex >= sleepDurations.length) {
    activeSleepDuration.value = null;
    sleepTimeRemaining.value = null;
    return; // Exit function, timer is now off
  }

  // 4. Set the new active duration and start the countdown
  activeSleepDuration.value = sleepDurations[nextIndex];
  sleepTimeRemaining.value = activeSleepDuration.value * 60;

  // 5. Start the countdown interval
  sleepTimerId.value = setInterval(() => {
    if (sleepTimeRemaining.value > 0) {
      sleepTimeRemaining.value--;
    } else {
      // Timer finished: pause the audio and reset timer state
      if (audioPlayer.value) {
        audioPlayer.value.pause();
        isPlaying.value = false;
      }
      clearInterval(sleepTimerId.value);
      sleepTimerId.value = null;
      activeSleepDuration.value = null;
      sleepTimeRemaining.value = null;
    }
  }, 1000); // Ticks every second
};

const pc_toggleFavorite = async () => {
  if (!selectedTrack.value || selectedTrack.value === 'LIVE_STREAM' || !favoritePlaylist.value) return;

  const track = selectedTrack.value;
  const index = favoritePlaylist.value.indexOf(track);

  if (index > -1) {
    favoritePlaylist.value.splice(index, 1);
  } else {
    favoritePlaylist.value.push(track);
  }

  await updateFavoritePlaylist();
};

const updateFavoritePlaylist = async () => {
  const token = localStorage.getItem('authToken');
  if (!token) return;

  try {
    await $fetch(`${apiBase}/pc_playlist_saveto_list/我的最愛`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ songs: favoritePlaylist.value })
    });
  } catch (err) {
    console.error('Error updating favorite playlist:', err);
  }
};

const formatTime = (seconds) => {
  if (isNaN(seconds) || seconds < 0) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

// Debugging event handlers
const onAudioError = (event) => {
  console.error('🎵 Audio error:', event);
  console.error('🎵 Audio error code:', audioPlayer.value?.error?.code);
  
  // Stop any loading indicators
  isLoading.value = false;
  loadingStreamTitle.value = null;
  clearTimeout(loadingTimer);
  isPlaying.value = false;
  
  // Clean up HLS if there was an error
  destroyHLS();
  
  // Inform the user with a specific message
  if (selectedTrack.value === 'LIVE_STREAM') {
    alert('The radio stream was interrupted or is unavailable. Please try reconnecting.');
  } else {
    alert('An error occurred while playing the track. It may be corrupted or unavailable.');
  }
};

const onCanPlayThrough = () => {
  console.log('🎵 Audio can play through - ready for smooth playback');
};
</script>

<style scoped>
/* Custom slider styling */
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
