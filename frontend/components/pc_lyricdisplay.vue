<template>
  <div v-if="lyrics.length > 0 && !isLiveStream" class="bg-white p-6 rounded-lg shadow-xl mt-6">
    <h3 class="text-xl font-bold mb-4 text-gray-800 text-center">Lyrics</h3>
    <div class="lyrics-container max-h-96 overflow-y-auto">
      <div 
        v-for="(line, index) in lyrics" 
        :key="index"
        :class="[
          'lyrics-line py-2 px-4 rounded transition-all duration-300 text-center',
          line.isActive ? 'bg-blue-100 text-blue-800 font-semibold transform scale-105' : 'text-gray-600'
        ]"
        :ref="line.isActive ? 'activeLyricLine' : null"
      >
        {{ line.text }}
      </div>
    </div>
    <div v-if="!lyricsLoaded && lyricsChecked" class="text-center text-gray-500 py-4">
      No lyrics file found for this track
    </div>
    <div v-if="!lyricsChecked" class="text-center text-gray-500 py-4">
      Checking for lyrics...
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

// Props
const props = defineProps({
  trackPath: {
    type: String,
    default: ''
  },
  currentTime: {
    type: Number,
    default: 0
  },
  isLiveStream: {
    type: Boolean,
    default: false
  },
  apiBase: {
    type: String,
    required: true
  }
});

// Reactive state
const lyrics = ref([]);
const lyricsLoaded = ref(false);
const lyricsChecked = ref(false);

// Parse LRC file content into an array of timed lyrics
const parseLRC = (lrcContent) => {
  const lines = lrcContent.split('\n');
  const parsedLyrics = [];
  
  // Regular expression to match time stamps [mm:ss.xx] or [mm:ss]
  const timeRegex = /\[(\d{2}):(\d{2})\.?(\d{2})?\]/g;
  
  lines.forEach(line => {
    const matches = [...line.matchAll(timeRegex)];
    if (matches.length > 0) {
      // Extract the text after removing all time stamps
      const text = line.replace(timeRegex, '').trim();
      if (text) {
        matches.forEach(match => {
          const minutes = parseInt(match[1], 10);
          const seconds = parseInt(match[2], 10);
          const centiseconds = match[3] ? parseInt(match[3], 10) : 0;
          const timeInSeconds = minutes * 60 + seconds + centiseconds / 100;
          
          parsedLyrics.push({
            time: timeInSeconds,
            text: text,
            isActive: false
          });
        });
      }
    }
  });
  
  // Sort by time
  parsedLyrics.sort((a, b) => a.time - b.time);
  return parsedLyrics;
};

// Load lyrics for the current track
const loadLyrics = async (trackPath) => {
  if (!trackPath || trackPath === 'LIVE_STREAM') {
    lyrics.value = [];
    lyricsLoaded.value = false;
    lyricsChecked.value = true;
    return;
  }
  
  lyricsChecked.value = false;
  lyricsLoaded.value = false;
  
  try {
    // Convert the track path to lyrics path by changing the extension
    const lrcPath = trackPath.replace(/\.(mp3|MP3|flac|FLAC)$/, '.lrc');
    
    // Try to fetch the LRC file
    const response = await fetch(`${props.apiBase}/music/${lrcPath}`);
    
    if (response.ok) {
      const lrcContent = await response.text();
      const parsedLyrics = parseLRC(lrcContent);
      
      if (parsedLyrics.length > 0) {
        lyrics.value = parsedLyrics;
        lyricsLoaded.value = true;
        console.log(`Lyrics loaded for ${trackPath}: ${parsedLyrics.length} lines`);
      } else {
        lyrics.value = [];
        lyricsLoaded.value = false;
      }
    } else {
      lyrics.value = [];
      lyricsLoaded.value = false;
    }
  } catch (error) {
    console.log(`No lyrics file found for ${trackPath}`);
    lyrics.value = [];
    lyricsLoaded.value = false;
  } finally {
    lyricsChecked.value = true;
  }
};

// Update active lyrics line based on current time
const updateActiveLyrics = (currentTime) => {
  if (lyrics.value.length === 0) return;
  
  let activeIndex = -1;
  
  // Find the active lyrics line
  for (let i = 0; i < lyrics.value.length; i++) {
    if (currentTime >= lyrics.value[i].time) {
      activeIndex = i;
    } else {
      break;
    }
  }
  
  // Update active state for all lines
  lyrics.value.forEach((line, index) => {
    line.isActive = index === activeIndex;
  });
  
  // Auto-scroll to active line in the next tick
  if (activeIndex >= 0) {
    nextTick(() => {
      const activeElement = document.querySelector('.lyrics-line.bg-blue-100');
      if (activeElement) {
   //     activeElement.scrollIntoView({ 
   //       behavior: 'smooth', 
   //       block: 'center' 
   //     });
      }
    });
  }
};

// Watch for track changes
watch(() => props.trackPath, (newTrackPath) => {
  if (newTrackPath && !props.isLiveStream) {
    loadLyrics(newTrackPath);
  } else {
    lyrics.value = [];
    lyricsLoaded.value = false;
    lyricsChecked.value = true;
  }
}, { immediate: true });

// Watch for time updates
watch(() => props.currentTime, (newTime) => {
  if (lyricsLoaded.value) {
    updateActiveLyrics(newTime);
  }
});
</script>

<style scoped>
/* Additional styling can be added here if needed */
</style>