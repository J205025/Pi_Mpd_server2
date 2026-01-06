<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-4 mb-4 p-2 sm:p-4 md:p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl flex flex-col sm:flex-row justify-between items-center relative">
        <div class="text-center sm:text-left sm:absolute sm:left-1/2 sm:-translate-x-1/2 w-full sm:w-auto mb-2 sm:mb-0">
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900">音響播放(Pi Player)</h1>
        </div>
        <div class="w-full sm:w-auto mt-2 sm:mt-0 sm:ml-auto p-2 border border-gray-300 rounded-lg text-sm bg-gray-50 shadow-inner">
          <div class="grid grid-cols-2 gap-x-4">
            <div class="font-bold">MPD Status:</div>
            <div class="text-right">
              <span 
                :class="{
                  'text-green-500': isMpdNormal, 
                  'text-red-500': !isMpdNormal
                }" 
                class="font-semibold"
              >
                {{ isMpdNormal ? 'Normal' : 'Abnormal' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-xl mt-4">
        <div class="text-center mb-4">
          <p v-if="isLiveStream" class="text-gray-600 font-bold">{{ channelName || displayTitle || 'Live Radio' }}</p>
          <p v-else class="text-gray-600 font-bold">{{ displayTitle }}</p>
          <p v-if="isLiveStream" class="text-gray-500 text-sm mt-1">Live Radio</p>
          <div v-else>
            <p class="text-gray-500 text-sm mt-1">{{ displayArtist }}</p>
            <p class="text-gray-500 text-sm mt-1">{{ displayAlbum }}</p>
          </div>
        </div>

        <div class="mb-6">
            <div v-if="!isLiveStream">
                <div class="flex justify-between text-sm text-gray-600 mb-2">
                    <span>{{ formatTime(elapsed) }}</span>
                    <span>{{ formatTime(duration) }}</span>
                </div>
                <div 
                    class="w-full bg-gray-200 rounded-full h-2 cursor-pointer"
                    @click="seek($event)"
                >
                    <div 
                        class="bg-blue-600 h-2 rounded-full transition-all duration-100"
                        :style="{ width: progressPercentage + '%' }"
                    ></div>
                </div>
            </div>

            <div v-else class="text-center py-2">
                <span class="text-red-500 font-bold text-lg animate-pulse">🔴 LIVE</span>
                <p class="text-gray-500 text-sm mt-1">Elapsed: {{ formatTime(elapsed) }}</p>
            </div>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-2 sm:space-x-4 mb-6">
          <button
            @click="prevSong"
            class="bg-gray-200 hover:bg-gray-300 p-2 sm:p-3 rounded-full transition-colors duration-200"
          >
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M8.445 14.832A1 1 0 0010 14v-2.798l5.445 3.63A1 1 0 0017 14V6a1 1 0 00-1.555-.832L10 8.798V6a1 1 0 00-1.555-.832l-6 4a1 1 0 000 1.664l6 4z"/>
            </svg>
          </button>

          <button
            @click="togglePlayPause"
            class="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-full bg-blue-500 hover:bg-blue-600 focus:outline-none text-white transition-colors duration-200 flex items-center justify-center shadow-lg"
          >
            <svg v-if="mpdStatus.state === 'play'" class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/>
            </svg>
            <svg v-else class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/>
            </svg>
          </button>

          <button
            @click="nextSong"
            class="bg-gray-200 hover:bg-gray-300 p-2 sm:p-3 rounded-full transition-colors duration-200"
          >
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z"/>
            </svg>
          </button>
          
          <!-- Regular Playlist Button -->
          <button @click="toggleRegularPlaylist" :disabled="!currentSong.file || isLiveStream" class="p-2 sm:p-3 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isCurrentSongInRegularPlaylist" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 text-green-500" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.539 1.118l-3.975-2.888a1 1 0 00-1.175 0l-3.976 2.888c-.783.57-1.838-.197-1.539-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </button>
          
          <!-- Favorite Button -->
          <button @click="toggleFavorite" :disabled="!currentSong.file || isLiveStream" class="p-2 sm:p-3 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isCurrentSongFavorite" class="w-5 h-5 sm:w-6 sm:w-6 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="w-5 h-5 sm:w-6 sm:h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 20 20">
              <path d="M17.5 9.16666C17.5 12.5 14.1667 15.8333 10 17.5C5.83333 15.8333 2.5 12.5 2.5 9.16666C2.5 7.04738 4.21401 5.33333 6.33333 5.33333C7.53594 5.33333 8.6425 5.84196 9.39999 6.69433L10 7.35766L10.6 6.69433C11.3575 5.84196 12.4641 5.33333 13.6667 5.33333C15.786 5.33333 17.5 7.04738 17.5 9.16666Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

          <div class="flex flex-wrap items-center justify-center mt-6 space-y-4 md:justify-between md:space-y-0">
            <div class="flex items-center space-x-2">
              <input
                type="range"
                min="0"
                max="100"
                step="1"
                v-model="volume"
                @input="setVolume"
                class="w-full sm:w-24 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              >
              <span class="text-sm text-gray-600 w-8">{{ volume }}</span>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-2">
              
              <button
                @click="toggleRandom"
                :class="['p-2 rounded-full transition-colors duration-200', mpdStatus.random == 1 ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800']"
              ><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732L14.146 12.8l-1.179 4.456a1 1 0 01-1.856-.288L12.382 12H10a1 1 0 110-2h2.382l-.271-4.968A1 1 0 0112 2z" clip-rule="evenodd"></path></svg></button>
              
              <button
                @click="toggleRepeat"
                :class="['p-2 rounded-full transition-colors duration-200', mpdStatus.repeat == 1 || mpdStatus.single == 1 ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800']"
              >
                <svg v-if="mpdStatus.single == 1" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5.05 4.05a7 7 0 000 9.9 7 7 0 009.9 0a1 1 0 111.414 1.414 9 9 0 01-12.728 0 9 9 0 010-12.728A9 9 0 0110 1.05a1 1 0 110 2 7 7 0 00-4.95 1zM14.95 15.95a7 7 0 000-9.9 7 7 0 00-9.9 0a1 1 0 11-1.414-1.414 9 9 0 0112.728 0 9 9 0 010 12.728A9 9 0 0110 18.95a1 1 0 110-2 7 7 0 004.95-1z"></path></svg>
                <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 12V7H3l4-4 4 4H9v5a1 1 0 01-1 1H5zm10 1v5h2l-4 4-4-4h2V8a1 1 0 011-1h3z"></path></svg>
              </button>

              <button
                @click="cycleSleepTimer"
                :class="['p-2 rounded w-24 sm:w-28 text-center transition-colors duration-200 font-semibold', activeSleepDuration ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200']"
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
          <span v-if="mpdStatus.playlistlength > 0">
            Track {{ parseInt(mpdStatus.song) + 1 }} of {{ mpdStatus.playlistlength }}
          </span>
          <span v-if="mpdStatus.random == 1" class="ml-2">(Shuffle)</span>
          <span v-if="mpdStatus.repeat == 1 && mpdStatus.single == 0" class="ml-2">(Repeat All)</span>
          <span v-if="mpdStatus.single == 1" class="ml-2">(Repeat One)</span>
        </div>
      </div>
      
      <!-- Stored Playlists Section -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-4">
        <label for="load-playlist-select" class="block text-xl font-bold mb-3 text-gray-800">選擇歌單:</label>
        <div class="flex space-x-2">
            <select
              id="load-playlist-select"
              v-model="selectedStoredPlaylist"
              @change="clearQueueAndLoadPlaylist"
              class="block w-full p-3 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            >
              <option disabled selected value="">-- Choose a playlist --</option>
              <option v-for="name in sortedStoredPlaylists" 
                      :key="name.playlist" 
                      :value="name.playlist"
                      :style="{ color: name.playlist === '我的最愛' ? 'red' : (name.playlist === '定期播放' ? 'green' : 'black') }">
                {{ name.playlist }}
              </option>
            </select>
        </div>
      </div>


      <!-- Current Playing Queue -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-6">
        <h2 class="text-xl font-bold mb-3 text-gray-800">播放佇列:</h2>
        <button @click="clearQueue" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mb-2">清空佇列</button>
        <div v-if="queue.length > 0" class="max-h-96 overflow-y-auto">
          <ul class="list-inside bg-gray-50 p-4 rounded-lg">
            <li v-for="song in queue" :key="song.id" 
                @click="playSongById(song.id)"
                class="text-gray-700 p-1 truncate cursor-pointer hover:bg-blue-100"
                :class="{ 'bg-blue-200': song.id == mpdStatus.songid }">
              {{ +song.pos + 1 }} - {{ song.file }}
            </li>
          </ul>
        </div>
        <div v-else class="text-gray-500">Queue is empty.</div>
      </div>

      <!-- Cron Job Section -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-4">
        <h2 class="text-xl font-bold mb-3 text-gray-800">定期播放設定:</h2>
        <div class="mb-4">
          <p v-if="cronJobs.length > 0" class="text-gray-600">
            目前設定: {{ formatCronSchedule(cronJobs[0].schedule) }}
          </p>
          <p v-else class="text-gray-500">
            尚未設定定期播放
          </p>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <div>
            <label for="cron-hour" class="block text-sm font-medium text-gray-700">小時 (0-23)</label>
            <input type="number" id="cron-hour" v-model.number="cronHour" min="0" max="23" class="mt-1 block w-full sm:w-24 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
          </div>
          <div>
            <label for="cron-minute" class="block text-sm font-medium text-gray-700">分鐘 (0-59)</label>
            <input type="number" id="cron-minute" v-model.number="cronMinute" min="0" max="59" class="mt-1 block w-full sm:w-24 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">重複頻率</label>
            <div class="mt-1 flex flex-wrap gap-2">
              <label v-for="(dayName, index) in daysOfWeek" :key="index" class="inline-flex items-center">
                <input
                  type="checkbox"
                  :value="index"
                  v-model="cronDayOfWeek"
                  class="form-checkbox h-4 w-4 text-blue-600"
                >
                <span class="ml-2 text-sm text-gray-700">{{ dayName }}</span>
              </label>
            </div>
          </div>
          <div class="pt-6 flex flex-col sm:flex-row gap-2">
            <button @click="setCronJob" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">設定更新定期播放</button>
            <button @click="deleteCronJob" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">刪除定期播放</button>
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-2">"定期播放" 歌單會被自動載入及播放. 如果 "定期播放" 歌單不存在, 將會已伺服器內"定期播放"資料夾內的歌曲自動建立.</p>
      </div>

      <pi_radiocard />

    </main>
    
    <footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter } from 'vue-router';
import pi_radiocard from '~/components/pi_radiocard.vue';

const channelName = useState('channelName');
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const router = useRouter();

const mpdStatus = ref({});
const currentSong = ref({});
const queue = ref([]);
const storedPlaylists = ref([]);
const selectedStoredPlaylist = ref('');
const cronJobs = ref([]);
const cronHour = ref(0);
const cronMinute = ref(0);
const cronDayOfWeek = ref([]); // 0=Sunday, 1=Monday, ..., 6=Saturday
const daysOfWeek = ['週日', '週一', '週二', '週三', '週四', '週五', '週六'];
const favoritePlaylistSongs = ref([]);
const regularPlaylistSongs = ref([]);
const userSettings = ref({
  id3tagDisplaytype: true,
});

const sleepDurations = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60];
const activeSleepDuration = ref(null);
const sleepTimeRemaining = ref(null);
const sleepTimerId = ref(null);

const volume = ref(0);
const duration = ref(0);
const elapsed = ref(0);
let pollInterval;

const isMpdNormal = computed(() => {
  return mpdStatus.value && Object.keys(mpdStatus.value).length > 0 && mpdStatus.value.state !== undefined;
});

const sortedStoredPlaylists = computed(() => {
  const playlists = [...storedPlaylists.value];
  const favoriteName = '我的最愛';
  const regularPlayName = '定期播放';

  let favoritePlaylist = null;
  let regularPlaylist = null;
  const otherPlaylists = [];

  playlists.forEach(p => {
    if (p.playlist === favoriteName) {
      favoritePlaylist = p;
    } else if (p.playlist === regularPlayName) {
      regularPlaylist = p;
    } else {
      otherPlaylists.push(p);
    }
  });

  const result = [];
  if (favoritePlaylist) {
    result.push(favoritePlaylist);
  }
  if (regularPlaylist) {
    result.push(regularPlaylist);
  }
  result.push(...otherPlaylists);
  
  return result;
});
const isLiveStream = computed(() => {
  return currentSong.value.file && (currentSong.value.file.startsWith('http://') || currentSong.value.file.startsWith('https://'));
});

const progressPercentage = computed(() => {
  return duration.value > 0 ? (elapsed.value / duration.value) * 100 : 0;
});

const displayTitle = computed(() => {
  if (!currentSong.value || !currentSong.value.file) return 'No song playing';
  if (userSettings.value.id3tagDisplaytype) {
    return currentSong.value.title || 'No song playing';
  }
  const parts = currentSong.value.file.split('/');
  if (parts.length > 0) {
    const fileName = parts[parts.length - 1];
    // Remove file extension
    return fileName.substring(0, fileName.lastIndexOf('.')) || fileName;
  }
  return 'No song playing';
});

const displayArtist = computed(() => {
  if (!currentSong.value || !currentSong.value.file) return '';
  if (userSettings.value.id3tagDisplaytype) {
    return currentSong.value.artist || '';
  }
  const parts = currentSong.value.file.split('/');
  if (parts.length >= 3) {
    return parts[parts.length - 3];
  }
  return '';
});

const displayAlbum = computed(() => {
  if (!currentSong.value || !currentSong.value.file) return '';
  if (userSettings.value.id3tagDisplaytype) {
    return currentSong.value.album || '';
  }
  const parts = currentSong.value.file.split('/');
  if (parts.length >= 2) {
    return parts[parts.length - 2];
  }
  return '';
});

const fetchUserSettings = async () => {
  const token = localStorage.getItem('authToken');
  if (!token) return;

  try {
    const response = await $fetch(`${apiBase}/users/me/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.settings) {
      userSettings.value = response.settings;
    }
  } catch (error) {
    console.error('Error fetching user settings:', error);
  }
};

const fetchMpdStatus = async () => {
  try {
    const response = await $fetch(`${apiBase}/pi_mpd_status`);
    mpdStatus.value = response;
    volume.value = response.volume;
    duration.value = parseFloat(response.duration) || 0;
    elapsed.value = parseFloat(response.elapsed) || 0;
    
    if (mpdStatus.value.songid) {
        fetchCurrentSong();
    } else {
        currentSong.value = {};
    }

  } catch (error) {
    console.error('Error fetching MPD status:', error);
  }
};

const fetchCurrentSong = async () => {
    try {
        const response = await $fetch(`${apiBase}/pi_queue_current_song`);
        currentSong.value = response;
    } catch (error) {
        console.error('Error fetching current song:', error);
        currentSong.value = {};
    }
}

const fetchQueue = async () => {
  try {
    const response = await $fetch(`${apiBase}/pi_queue_songs`);
    queue.value = response;
  } catch (error) {
    console.error('Error fetching queue:', error);
  }
};

const fetchStoredPlaylists = async () => {
  try {
    const response = await $fetch(`${apiBase}/pi_get_playlists_List`);
    storedPlaylists.value = response;
  } catch (error) {
    console.error('Error fetching stored playlists:', error);
  }
};

const fetchPlaylistSongs = async (playlistName) => {
  try {
    const response = await $fetch(`${apiBase}/pi_playlist_songs/${encodeURIComponent(playlistName)}`);
    return response; 
  } catch (error) {
    console.error(`Error fetching songs for playlist ${playlistName}:`, error);
    return [];
  }
};

const fetchCronJobs = async () => {
  try {
    const response = await $fetch(`${apiBase}/api/cron`);
    cronJobs.value = response;
    if (response.length > 0) {
      const schedule = response[0].schedule;
      // Example schedule: "0 8 * * *"
      const parts = schedule.split(' ');
      cronMinute.value = parseInt(parts[0], 10);
      cronHour.value = parseInt(parts[1], 10);
      const dayOfWeekPart = parts[4];
      if (dayOfWeekPart === '*') {
        cronDayOfWeek.value = [0, 1, 2, 3, 4, 5, 6];
      } else {
        cronDayOfWeek.value = dayOfWeekPart.split(',').map(Number);
      }
    }
  } catch (error) {
    console.error('Error fetching cron jobs:', error);
  }
};

const setCronJob = async () => {
  if (cronHour.value < 0 || cronHour.value > 23 || cronMinute.value < 0 || cronMinute.value > 59) {
    alert('Invalid hour or minute.');
    return;
  }
  try {
    await $fetch(`${apiBase}/api/cron`, {
      method: 'POST',
      body: { hour: cronHour.value, minute: cronMinute.value, day_of_week: cronDayOfWeek.value }
    });
    fetchCronJobs();
  } catch (error) {
    console.error('Error setting cron job:', error);
    alert('Failed to set cron job.');
  }
};

const deleteCronJob = async () => {
  if (!confirm('Are you sure you want to delete the scheduled job?')) return;
  try {
    await $fetch(`${apiBase}/api/cron`, { method: 'DELETE' });
    cronJobs.value = []; // Clear local display
    cronHour.value = 0;
    cronMinute.value = 0;
    cronDayOfWeek.value = [];
  } catch (error) {
    console.error('Error deleting cron job:', error);
    alert('Failed to delete cron job.');
  }
};

const formatCronSchedule = (schedule) => {
  if (!schedule) return 'Not set';
  const parts = schedule.split(' ');
  const minute = parts[0];
  const hour = parts[1];
  const dayOfWeekPart = parts[4];

  let days = '';
  if (dayOfWeekPart === '*') {
    days = '每天';
  } else {
    const selectedDays = dayOfWeekPart.split(',').map(Number);
    if (selectedDays.length === 7) {
      days = '每天';
    } else {
      days = selectedDays.map(dayIndex => daysOfWeek[dayIndex]).join(', ');
    }
  }

  return `${days} ${hour.padStart(2, '0')}:${minute.padStart(2, '0')}`;
};

const isCurrentSongFavorite = computed(() => {
  if (!currentSong.value.file) return false;
  return favoritePlaylistSongs.value.includes(currentSong.value.file);
});

const isCurrentSongInRegularPlaylist = computed(() => {
  if (!currentSong.value.file) return false;
  return regularPlaylistSongs.value.includes(currentSong.value.file);
});

const togglePlayPause = async () => {
  try {
    await $fetch(`${apiBase}/pi_pause`, { method: 'POST' });
    fetchMpdStatus();
  } catch (error)
 {
    console.error('Error toggling play/pause:', error);
  }
};

const nextSong = async () => {
  try {
    await $fetch(`${apiBase}/pi_next`, { method: 'POST' });
    fetchMpdStatus();
  } catch (error) {
    console.error('Error playing next song:', error);
  }
};

const prevSong = async () => {
  try {
    await $fetch(`${apiBase}/pi_prev`, { method: 'POST' });
    fetchMpdStatus();
  } catch (error) {
    console.error('Error playing previous song:', error);
  }
};

const setVolume = async () => {
  try {
    await $fetch(`${apiBase}/pi_setvol/${volume.value}`, { method: 'PUT' });
  }  catch (error) {
    console.error('Error setting volume:', error);
  }
};

const seek = async (event) => {
    if (duration.value === 0) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const percentage = (event.clientX - rect.left) / rect.width;
    const time = percentage * duration.value;
    try {
        await $fetch(`${apiBase}/pi_seekcur/${time}`, { method: 'PUT' });
        fetchMpdStatus();
    } catch (error) {
        console.error('Error seeking:', error);
    }
}

const playSongById = async (songId) => {
    try {
        await $fetch(`${apiBase}/pi_playid/${songId}`, { method: 'POST' });
        fetchMpdStatus();
    } catch (error) {
        console.error('Error playing song by id:', error);
    }
}

const clearQueue = async () => {
    if (!confirm('Are you sure you want to clear the queue?')) return;
    try {
        await $fetch(`${apiBase}/pi_queue_clearsongs`, { method: 'DELETE' });
        fetchQueue();
        fetchMpdStatus();
    } catch (error) {
        console.error('Error clearing queue:', error);
    }
}

const clearQueueAndLoadPlaylist = async () => {
    if (!selectedStoredPlaylist.value) {
        return;
    }
    try {
        // 1. Clear the queue (without confirmation)
        await $fetch(`${apiBase}/pi_queue_clearsongs`, { method: 'DELETE' });

        // 2. Load the new playlist
        await $fetch(`${apiBase}/pi_queue_loadfrom_playlist/${selectedStoredPlaylist.value}`, { method: 'GET' });

        // 3. Refresh queue and status
        fetchQueue();
        fetchMpdStatus();
    } catch (error) {
        console.error('Error clearing queue and loading playlist:', error);
    }
}

const toggleRepeat = async () => {
    const isRepeat = mpdStatus.value.repeat == 1;
    const isSingle = mpdStatus.value.single == 1;

    let nextRepeat = 0;
    let nextSingle = 0;

    if (!isRepeat && !isSingle) {
        // From None to Repeat All
        nextRepeat = 1;
        nextSingle = 0;
    } else if (isRepeat && !isSingle) {
        // From Repeat All to Repeat One
        nextRepeat = 1;
        nextSingle = 1;
    } else { // isSingle is true
        // From Repeat One to None
        nextRepeat = 0;
        nextSingle = 0;
    }

    try {
        await $fetch(`${apiBase}/pi_playmode?repeat=${nextRepeat}&single=${nextSingle}`, { method: 'PUT' });
        fetchMpdStatus();
    } catch (error) {
        console.error('Error toggling repeat mode:', error);
    }
}

const toggleRandom = async () => {
    const randomState = mpdStatus.value.random == 1 ? 0 : 1;
    try {
        await $fetch(`${apiBase}/pi_playmode?random=${randomState}`, { method: 'PUT' });
        fetchMpdStatus();
    } catch (error) {
        console.error('Error toggling random:', error);
    }
}

const cycleSleepTimer = () => {
  if (sleepTimerId.value) {
    clearInterval(sleepTimerId.value);
    sleepTimerId.value = null;
  }

  let nextIndex;
  if (activeSleepDuration.value === null) {
    nextIndex = 0;
  } else {
    const currentIndex = sleepDurations.indexOf(activeSleepDuration.value);
    nextIndex = currentIndex + 1;
  }

  if (nextIndex >= sleepDurations.length) {
    activeSleepDuration.value = null;
    sleepTimeRemaining.value = null;
    return;
  }

  activeSleepDuration.value = sleepDurations[nextIndex];
  sleepTimeRemaining.value = activeSleepDuration.value * 60;

  sleepTimerId.value = setInterval(async () => {
    if (sleepTimeRemaining.value > 0) {
      sleepTimeRemaining.value--;
    } else {
      try {
        await $fetch(`${apiBase}/pi_pause`, { method: 'POST' });
        fetchMpdStatus();
      } catch (error) {
        console.error('Error stopping player from sleep timer:', error);
      }
      clearInterval(sleepTimerId.value);
      sleepTimerId.value = null;
      activeSleepDuration.value = null;
      sleepTimeRemaining.value = null;
    }
  }, 1000);
};

const toggleFavorite = async () => {
  if (!currentSong.value || !currentSong.value.file || isLiveStream.value) {
    alert('No song selected or it is a live stream.');
    return;
  }

  const playlistName = '我的最愛';
  const songFile = currentSong.value.file;

  try {
    // Refresh the playlist songs before checking
    favoritePlaylistSongs.value = await fetchPlaylistSongs(playlistName);
    const songIndex = favoritePlaylistSongs.value.indexOf(songFile);

    if (songIndex !== -1) {
      // Song is in favorites, so remove it
      await $fetch(`${apiBase}/pi_playlistdeletesong`, {
        method: 'POST',
        body: { pi_plname: playlistName, songpos: songIndex }
      });

    } else {
      // Song is not in favorites, so add it
      await $fetch(`${apiBase}/pi_playlist_adduri/${encodeURIComponent(playlistName)}/${encodeURIComponent(songFile)}`, {
        method: 'POST',
      });

    }

    // Refresh favorite songs list to update UI
    favoritePlaylistSongs.value = await fetchPlaylistSongs(playlistName);
  } catch (error) {
    console.error('Error toggling favorite status:', error);
    alert('Failed to update favorites.');
  }
};

const toggleRegularPlaylist = async () => {
  if (!currentSong.value || !currentSong.value.file || isLiveStream.value) {
    alert('No song selected or it is a live stream.');
    return;
  }

  const playlistName = '定期播放';
  const songFile = currentSong.value.file;

  try {
    // Refresh the playlist songs before checking
    regularPlaylistSongs.value = await fetchPlaylistSongs(playlistName);
    const songIndex = regularPlaylistSongs.value.indexOf(songFile);

    if (songIndex !== -1) {
      // Song is in playlist, so remove it
      await $fetch(`${apiBase}/pi_playlistdeletesong`, {
        method: 'POST',
        body: { pi_plname: playlistName, songpos: songIndex }
      });

    } else {
      // Song is not in playlist, so add it
      await $fetch(`${apiBase}/pi_playlist_adduri/${encodeURIComponent(playlistName)}/${encodeURIComponent(songFile)}`, {
        method: 'POST',
      });

    }

    // Refresh regular playlist songs list to update UI
    regularPlaylistSongs.value = await fetchPlaylistSongs(playlistName);
  } catch (error) {
    console.error('Error toggling regular playlist status:', error);
    alert('Failed to update regular playlist.');
  }
};


const formatTime = (seconds) => {
  if (isNaN(seconds) || seconds < 0) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

onMounted(async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        router.push('/login');
        return;
    }
    await fetchMpdStatus();
    fetchQueue();
    fetchStoredPlaylists();
    fetchCronJobs();
    fetchUserSettings();
    favoritePlaylistSongs.value = await fetchPlaylistSongs('我的最愛'); // Fetch favorite songs on mount
    regularPlaylistSongs.value = await fetchPlaylistSongs('定期播放');
    pollInterval = setInterval(() => {
        fetchMpdStatus();
        fetchQueue(); // To keep queue updated
    }, 1000); // Poll every 3 seconds
});

onBeforeUnmount(() => {
  clearInterval(pollInterval);
  if (sleepTimerId.value) {
    clearInterval(sleepTimerId.value);
  }
});

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