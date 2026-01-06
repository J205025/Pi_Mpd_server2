<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl text-center">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">電腦歌單 (PC Playlist)</h1>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-xl mt-12">
        <h2 class="text-2xl font-bold text-gray-800">建立歌單:</h2>
        <div class="flex flex-col sm:flex-row gap-4">
          <button
            @click="openFileBrowser"
            :disabled="isLoading"
            class="bg-blue-500 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-600 disabled:bg-gray-400 transition duration-300"
          >
            瀏覽伺服器檔案
          </button>
          <button @click="autoDownloadPodcast()" class="bg-purple-600 text-white py-3 px-6 rounded-lg text-m hover:bg-purple-700 transition duration-300">下載播客</button>
        </div>

        <div v-if="errorMessage" class="mt-4 text-red-600 bg-red-100 p-3 rounded-lg">
          {{ errorMessage }}
        </div>
        
        <div v-if="fileList.length > 0" class="mt-6">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-800 mb-3">Generated Files:</h3>
          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="(file, index) in fileList" :key="index" 
                class="text-gray-700 p-1 truncate cursor-pointer"
                :class="{ 'bg-blue-200': filesToSaveFromFolder.includes(file) }"
                @click="toggleSelectionForFolderFiles(file)">
              {{ file }}
            </li>
          </ul>
          <div class="mt-4 flex flex-wrap justify-center gap-2 sm:gap-4">
            <button 
              @click="selectAllFolderFiles"
              class="bg-yellow-600 text-white font-bold py-2 px-4 sm:py-3 sm:px-6 text-sm sm:text-base rounded-lg hover:bg-yellow-700 transition duration-300"
            >
              Select All
            </button>
            <button 
              @click="deselectAllFolderFiles"
              class="bg-yellow-600 text-white font-bold py-2 px-4 sm:py-3 sm:px-6 text-sm sm:text-base rounded-lg hover:bg-yellow-700 transition duration-300"
            >
              Deselect All
            </button>
            <button 
              @click="promptForPlaylistName"
              :disabled="filesToSaveFromFolder.length === 0"
              class="bg-green-600 text-white font-bold py-2 px-4 sm:py-3 sm:px-6 text-sm sm:text-base rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition duration-300"
            >
              存入歌單
            </button>
          </div>
        </div>
      </div>

      <!-- Playlist List Section -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">你的歌單:(點歌單名字可編輯曲目)</h2>
        <div v-if="playlistsList.length > 0">
          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="(playlistName, index) in sortedPlaylists" :key="index"
                class="flex items-center text-gray-700 p-2 border-b border-gray-200 last:border-b-0">
              <span
                class="cursor-pointer hover:text-blue-600 font-medium"
                @click="getPlaylistFiles(playlistName)"
                :class="{
                  'bg-blue-200': playlistName === currentSelectedPlaylist,
                  'text-red-600': playlistName === '我的最愛'
                }">
                {{ playlistName }}
              </span>
              <div class="flex ml-auto" v-if="playlistName !== '我的最愛'">
                <button @click="promptRenamePlaylist(playlistName)" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">
                  更名
                </button>
                <button @click="deletePlaylist(playlistName)" class="bg-red-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-red-600 transition duration-300 mr-2">
                  刪除
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else class="text-gray-600 p-4 text-center">
          No playlists saved yet.
        </div>

        <div v-if="selectedPlaylistFiles.length > 0" class="mt-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-3">歌單-{{ currentSelectedPlaylist }}:</h3>
          
          <div class="mb-4">
            <button 
              @click="editModeForPlaylist = !editModeForPlaylist; selectedFilesInEditMode = []"
              class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300 mr-2"
            >
              {{ editModeForPlaylist ? '離開編輯' : '編輯' }}
            </button>
            <button 
              v-if="editModeForPlaylist"
              @click="deleteSelectedFilesFromPlaylist"
              :disabled="selectedFilesInEditMode.length === 0"
              class="bg-red-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-700 disabled:bg-gray-400 transition duration-300"
            >
              刪除
            </button>
            <button 
              v-if="editModeForPlaylist"
              @click="promptToSaveSelection"
              :disabled="selectedFilesInEditMode.length === 0"
              class="bg-green-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition duration-300 ml-2"
            >
              儲存
            </button>
          </div>

          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="(file, index) in selectedPlaylistFiles" :key="index" 
                class="text-gray-700 p-1 truncate"
                :class="{ 'bg-red-300 cursor-pointer': editModeForPlaylist && selectedFilesInEditMode.includes(file), 'cursor-pointer': editModeForPlaylist && !selectedFilesInEditMode.includes(file), 'cursor-default': !editModeForPlaylist }"
                @click="editModeForPlaylist ? toggleFileSelectionInEditMode(file) : null">
              {{ file }}
            </li>
          </ul>
        </div>
      </div>


      <div v-if="showSaveDialog" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <h3 class="text-xl font-bold mb-4">Enter Playlist Name</h3>
          <input 
            type="text"
            v-model="newPlaylistName"
            placeholder="My Awesome Playlist"
            class="w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div class="flex justify-end gap-4">
            <button @click="showSaveDialog = false" class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
            <button @click="savePlaylist" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
          </div>
        </div>
      </div>

      <div v-if="showRenameDialog" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <h3 class="text-xl font-bold mb-4">Rename Playlist: "{{ playlistToRename }}"</h3>
          <input 
            type="text"
            v-model="newPlaylistNameInput"
            placeholder="Enter new playlist name"
            class="w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div class="flex justify-end gap-4">
            <button @click="showRenameDialog = false" class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
            <button @click="confirmRename" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Rename</button>
          </div>
        </div>
      </div>

      <!-- File Browser Dialog -->
      <div v-if="showFileBrowser" class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-xl w-11/12 md:w-2/3 lg:w-1/2 max-h-[80vh] flex flex-col">
            <h3 class="text-xl font-bold mb-4">Browse Server Files</h3>
            <div class="mb-2 p-2 bg-gray-100 rounded-md text-sm text-gray-700 break-words">
                Current Path: /{{ currentPath }}
            </div>
            <div class="flex-grow overflow-y-auto border border-gray-200 rounded-lg p-4">
                <button @click="goUpDirectory" :disabled="!currentPath"
                    class="mb-4 bg-gray-200 text-gray-700 py-1 px-3 rounded-lg hover:bg-gray-300 disabled:bg-gray-100 disabled:text-gray-400">
                    ../
                </button>
                <p v-if="isLoading" class="text-gray-500">Loading files...</p>
                <ul v-else-if="fileBrowserItems.length > 0">
                    <li v-for="item in fileBrowserItems" :key="item.path"
                        class="flex items-center p-1 rounded-md"
                        :class="{ 'hover:bg-gray-200': true, 'bg-blue-200': selectedFileBrowserItems.some(it => it.path === item.path) }">
                        <input type="checkbox" v-model="selectedFileBrowserItems" :value="item" class="mr-3" @click.stop>
                        <span @click="item.type === 'directory' ? browseDirectory(item.path) : null"
                            class="flex-grow cursor-pointer">
                            <span class="mr-2">{{ item.type === 'directory' ? '📁' : '🎵' }}</span>
                            {{ item.name }}
                        </span>
                    </li>
                </ul>
                <p v-else class="text-gray-500">No files found or directory is empty.</p>
            </div>
            <div class="flex justify-end gap-4 mt-4">
                <button @click="showFileBrowser = false"
                    class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
                <button @click="addSelectedFilesToGeneratedList"
                    class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Add Selected</button>
            </div>
        </div>
      </div>



    </main>

    <footer />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const folderName = ref('');
const fileList = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const filesToSaveFromFolder = ref([]); // Renamed from selectedFiles
const showSaveDialog = ref(false);
const newPlaylistName = ref('');
const showRenameDialog = ref(false); // New state for rename dialog
const playlistToRename = ref('');    // New state to hold the name of the playlist being renamed
const newPlaylistNameInput = ref(''); // New state for the input field in rename dialog

// New state variables for playlist list and selected playlist files
const playlistsList = ref([]);
const selectedPlaylistFiles = ref([]);
const currentSelectedPlaylist = ref('');
const selectedFilesInEditMode = ref([]); // To track files selected for deletion from an opened playlist
const editModeForPlaylist = ref(false); // To enable/disable editing mode for playlist files

// File Browser state
const showFileBrowser = ref(false);
const fileBrowserItems = ref([]);
const selectedFileBrowserItems = ref([]);
const currentPath = ref('');


const sortedPlaylists = computed(() => {
  const playlists = [...playlistsList.value];
  const favorite = '我的最愛';
  
  const favoritePlaylist = playlists.filter(p => p === favorite);
  const otherPlaylists = playlists.filter(p => p !== favorite);
  
  return [...favoritePlaylist, ...otherPlaylists];
});

// Function to fetch the list of playlist names
const getPlaylistsList = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_get_playlist_List`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    playlistsList.value = data.names; // Assuming the API returns { names: [...] }

  } catch (error) {
    console.error('Failed to fetch playlists list:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Function to fetch files for a specific playlist
const getPlaylistFiles = async (playlistName) => {
  isLoading.value = true;
  errorMessage.value = '';
  selectedPlaylistFiles.value = [];
  currentSelectedPlaylist.value = playlistName;
  selectedFilesInEditMode.value = []; // Clear selections for deletion when new playlist is loaded
  editModeForPlaylist.value = false; // Exit edit mode when new playlist is loaded

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_playlist_files/${encodeURIComponent(playlistName)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    selectedPlaylistFiles.value = data;

  } catch (error) {
    console.error(`Failed to fetch files for playlist ${playlistName}:`, error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Function to delete a playlist
const deletePlaylist = async (playlistName) => {
  if (!confirm(`Are you sure you want to delete the playlist "${playlistName}"?`)) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_playlist_rmpl/${encodeURIComponent(playlistName)}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    alert(`Playlist "${playlistName}" deleted successfully!`);
    await getPlaylistsList(); // Refresh the playlist list
    selectedPlaylistFiles.value = []; // Clear displayed files if the deleted playlist was selected
    currentSelectedPlaylist.value = '';
    selectedFilesInEditMode.value = [];
    editModeForPlaylist.value = false;

  } catch (error) {
    console.error(`Failed to delete playlist ${playlistName}:`, error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Function to fetch files for a specific playlist internally (without affecting UI state)
const fetchPlaylistContent = async (playlistName) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_playlist_files/${encodeURIComponent(playlistName)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    return await response.json();

  } catch (error) {
    console.error(`Failed to fetch content for playlist ${playlistName}:`, error);
    throw error;
  }
};

// Function to prompt for renaming a playlist
const promptRenamePlaylist = (oldPlaylistName) => {
  playlistToRename.value = oldPlaylistName;
  newPlaylistNameInput.value = oldPlaylistName; // Pre-fill with old name
  showRenameDialog.value = true;
};

// Function to confirm and perform the rename operation
const confirmRename = async () => {
  if (!newPlaylistNameInput.value.trim()) {
    alert('New playlist name cannot be empty.');
    return;
  }
  if (newPlaylistNameInput.value === playlistToRename.value) {
    alert('New playlist name is the same as the old name.');
    showRenameDialog.value = false;
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    // 1. Fetch the content of the old playlist
    const playlistContent = await fetchPlaylistContent(playlistToRename.value);

    // 2. Delete the old playlist
    const deleteResponse = await fetch(`${apiBase}/pc_playlist_rmpl/${encodeURIComponent(playlistToRename.value)}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!deleteResponse.ok) {
      const errorData = await deleteResponse.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status during delete: ${deleteResponse.status}`);
    }

    // 3. Save the content as a new playlist with the new name
    const saveResponse = await fetch(`${apiBase}/pc_playlist_saveto_list/${encodeURIComponent(newPlaylistNameInput.value)}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ songs: playlistContent })
    });

    if (!saveResponse.ok) {
      const errorData = await saveResponse.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status during save: ${saveResponse.status}`);
    }

    alert(`Playlist "${playlistToRename.value}" successfully renamed to "${newPlaylistNameInput.value}"!`);
    showRenameDialog.value = false;
    playlistToRename.value = '';
    newPlaylistNameInput.value = '';
    await getPlaylistsList(); // Refresh the playlist list
    selectedPlaylistFiles.value = []; // Clear displayed files if the renamed playlist was selected
    currentSelectedPlaylist.value = '';

  } catch (error) {
    console.error('Failed to rename playlist:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};


const pc_getFiles = async () => {
  if (!folderName.value.trim()) {
    errorMessage.value = 'Folder name cannot be empty.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  fileList.value = [];
  filesToSaveFromFolder.value = [];

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }
    
    const response = await fetch(`${apiBase}/pc_gen_fileslist/${encodeURIComponent(folderName.value)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    fileList.value = data;

  } catch (error) {
    console.error('Failed to fetch files:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Toggle selection for files generated from a folder
const toggleSelectionForFolderFiles = (file) => {
  const index = filesToSaveFromFolder.value.indexOf(file);
  if (index > -1) {
    filesToSaveFromFolder.value.splice(index, 1);
  } else {
    filesToSaveFromFolder.value.push(file);
  }
};

// Select all files generated from a folder
const selectAllFolderFiles = () => {
  filesToSaveFromFolder.value = [...fileList.value];
};

// Deselect all files generated from a folder
const deselectAllFolderFiles = () => {
  filesToSaveFromFolder.value = [];
};


// Toggle selection for files within a saved playlist (for deletion)
const toggleFileSelectionInEditMode = (file) => {
  const index = selectedFilesInEditMode.value.indexOf(file);
  if (index > -1) {
    selectedFilesInEditMode.value.splice(index, 1);
  } else {
    selectedFilesInEditMode.value.push(file);
  }
};

// Function to delete selected files from the currently viewed playlist
const deleteSelectedFilesFromPlaylist = async () => {
  if (!confirm(`Are you sure you want to delete the selected ${selectedFilesInEditMode.value.length} file(s) from "${currentSelectedPlaylist.value}"?`)) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    // Filter out the files marked for deletion
    const updatedFiles = selectedPlaylistFiles.value.filter(
      file => !selectedFilesInEditMode.value.includes(file)
    );

    await updatePlaylistContent(currentSelectedPlaylist.value, updatedFiles);
    alert('Selected files deleted and playlist updated successfully!');
    
    // Refresh the displayed files and exit edit mode
    await getPlaylistFiles(currentSelectedPlaylist.value);
    selectedFilesInEditMode.value = [];
    editModeForPlaylist.value = false;

  } catch (error) {
    console.error('Failed to delete files from playlist:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const promptToSaveSelection = () => {
  const newPlaylistName = prompt('Enter a name for the new playlist:');
  if (newPlaylistName && newPlaylistName.trim()) {
    saveSelectedFilesAsNewPlaylist(newPlaylistName.trim());
  }
};

const saveSelectedFilesAsNewPlaylist = async (playlistName) => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    await updatePlaylistContent(playlistName, selectedFilesInEditMode.value);
    alert(`Selected files saved to new playlist "${playlistName}" successfully!`);
    
    // Refresh the playlist list and exit edit mode
    await getPlaylistsList();
    selectedFilesInEditMode.value = [];
    editModeForPlaylist.value = false;

  } catch (error) {
    console.error('Failed to save selected files to new playlist:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Helper function to update playlist content on the backend
const updatePlaylistContent = async (playlistName, content) => {
  const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_playlist_saveto_list/${encodeURIComponent(playlistName)}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ songs: content })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }
}


const promptForPlaylistName = () => {
  showSaveDialog.value = true;
};

const savePlaylist = async () => {
  if (!newPlaylistName.value.trim()) {
    alert('Playlist name cannot be empty.');
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_playlist_saveto_list/${encodeURIComponent(newPlaylistName.value)}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ songs: filesToSaveFromFolder.value }) // Use filesToSaveFromFolder
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    alert('Playlist saved successfully!');
    showSaveDialog.value = false;
    newPlaylistName.value = '';
    filesToSaveFromFolder.value = [];
    await getPlaylistsList(); // Refresh the playlist list after saving

  } catch (error) {
    console.error('Failed to save playlist:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Fetch playlists on component mount
onMounted(() => {
  getPlaylistsList();
});

const autoDownloadPodcast = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/download_podcast`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    alert(data.message || 'Podcast download process completed.');

  } catch (error) {
    console.error('Failed to start podcast download:', error);
    errorMessage.value = error.message;
    alert(`Failed to start podcast download: ${error.message}`);
  } finally {
    isLoading.value = false;
  }
};

const openFileBrowser = () => {
    showFileBrowser.value = true;
    browseDirectory('');
};

const browseDirectory = async (path) => {
    isLoading.value = true;
    errorMessage.value = '';
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
          throw new Error("Authentication token is not available. Please log in.");
        }
        const response = await fetch(`${apiBase}/pc_browse/${encodeURIComponent(path)}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to browse files');
        fileBrowserItems.value = await response.json();
        currentPath.value = path;
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        isLoading.value = false;
    }
};

const goUpDirectory = () => {
    if (!currentPath.value) return;
    const parentPath = currentPath.value.substring(0, currentPath.value.lastIndexOf('/'));
    browseDirectory(parentPath);
};

const getFilesInDirectory = async (directoryPath) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }
    const response = await fetch(`${apiBase}/pc_browse/${encodeURIComponent(directoryPath)}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error(`Failed to browse directory ${directoryPath}`);
    const items = await response.json();
    
    let files = [];
    for (const item of items) {
        if (item.type === 'file') {
            files.push(item.path);
        } else if (item.type === 'directory') {
            // Recursively get files from subdirectory
            const subDirFiles = await getFilesInDirectory(item.path);
            files = files.concat(subDirFiles);
        }
    }
    return files;
  } catch (error) {
    console.error(`Error getting files from directory ${directoryPath}:`, error);
    errorMessage.value = error.message;
    return [];
  }
};

const addSelectedFilesToGeneratedList = async () => {
    if (selectedFileBrowserItems.value.length === 0) {
        alert('No files selected.');
        return;
    }
    isLoading.value = true;
    const newFilesToAdd = [];
    for (const item of selectedFileBrowserItems.value) {
        if (item.type === 'file') {
            newFilesToAdd.push(item.path);
        } else if (item.type === 'directory') {
            const filesInDir = await getFilesInDirectory(item.path);
            newFilesToAdd.push(...filesInDir);
        }
    }
    // Add to fileList, avoiding duplicates
    newFilesToAdd.forEach(file => {
      if (!fileList.value.includes(file)) {
        fileList.value.push(file);
      }
    });

    showFileBrowser.value = false;
    selectedFileBrowserItems.value = [];
    isLoading.value = false;
};

</script>

<style scoped>
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
