# my_package/mpd_controller.py
import os
import sys
from pathlib import Path # Added import
from mpd import MPDClient
from mpd import ConnectionError as MPDConnectionError
from mpd import CommandError as MPDCommandError

class MPDClientController:
    """
    A class to control the Music Player Daemon (MPD) using python-mpd2.
    Includes auto-reconnection logic to prevent crashes after idle periods.
    """

    def __init__(self, host='localhost', port=6600, music_base_path='/home/ubuntu/Music/'):
        self.host = host
        self.port = port
        self.music_base_path = music_base_path
        self.client = MPDClient(use_unicode=True)
        # We track connection state, but we also verify it with ping()
        self.is_connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Connects to the MPD server.
        Checks if the connection is actually alive using ping().
        """
        # 1. If we think we are connected, verify it.
        if self.is_connected:
            try:
                self.client.ping()
                # If ping succeeds, we are good.
                return
            except (MPDConnectionError, OSError):
                print("Connection flag was True, but ping failed. Reconnecting...")
                self.is_connected = False
                try:
                    self.client.disconnect()
                except:
                    pass

        # 2. Perform fresh connection
        print(f"Attempting to connect to MPD at {self.host}:{self.port}...")
        try:
            self.client.connect(self.host, self.port)
            self.is_connected = True
            print("Successfully connected to MPD.")
        except MPDConnectionError as e:
            print(f"Error: Could not connect to MPD. {e}")
            self.is_connected = False
            # We do not raise here to allow the app to start even if MPD is temporarily down
        except Exception as e:
            print(f"An unexpected error occurred during connection: {e}")
            self.is_connected = False

    def disconnect(self):
        """Disconnects from the MPD server."""
        try:
            self.client.close()
            self.client.disconnect()
        except:
            pass
        finally:
            self.is_connected = False
            print("Disconnected from MPD.")

    def _execute_safe(self, func, *args, **kwargs):
        """
        Wraps MPD commands to handle disconnection/reconnection automatically.
        """
        try:
            if not self.is_connected:
                self.connect()
            return func(*args, **kwargs)
        except (MPDConnectionError, OSError, ConnectionRefusedError):
            print("Connection lost during command. Attempting to reconnect...")
            self.is_connected = False
            try:
                self.connect()
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Reconnection failed: {e}")
                # We return None or empty structures based on context usually, 
                # but raising allows the API to send a 500 error if really needed.
                raise e

    # --- Status & Playback ---

    def get_status(self):
        try:
            status = self._execute_safe(self.client.status)
            # Optional: Print status for debug, or comment out to reduce noise
            # print("--- Player Status ---")
            # for key, value in status.items():
            #     print(f"{key.capitalize()}: {value}")
            return status
        except Exception as e:
            print(f"Command Error in get_status: {e}")
            return None
        
    def update(self):
        try:
            self._execute_safe(self.client.update)
            print("MPD database update command sent.")
        except Exception as e:
            print(f"Error: {e}")



    def play(self):
        try:
            self._execute_safe(self.client.play)
            print("Playback started.")
        except Exception as e:
            print(f"Error: {e}")

    def pause(self):
        try:
            self._execute_safe(self.client.pause)
            print("Playback paused/unpaused.")
        except Exception as e:
            print(f"Error: {e}")

    def stop(self):
        try:
            self._execute_safe(self.client.stop)
            print("Playback stopped.")
        except Exception as e:
            print(f"Error: {e}")

    def next(self):
        try:
            self._execute_safe(self.client.next)
            print("Skipped to the next song.")
        except Exception as e:
            print(f"Error: {e}")
    
    def prev(self):
        try:
            self._execute_safe(self.client.previous)
            print("Skipped to the previous song.")
        except Exception as e:
            print(f"Error: {e}")

    def setvol(self, volume):
        try:
            volume = int(volume)
            if 0 <= volume <= 100:
                self._execute_safe(self.client.setvol, volume)
                print(f"Volume set to {volume}.")
            else:
                print("Error: Volume must be an integer between 0 and 100.")
        except Exception as e:
            print(f"Error setting volume: {e}")


    # --- Modes ---

    def random(self, state):
        try:
            self._execute_safe(self.client.random, state)
            print(f"Set random mode to {'on' if state else 'off'}.")
        except Exception as e: print(f"Error: {e}")

    def single(self, state):
        try:
            self._execute_safe(self.client.single, state)
            print(f"Set single mode to {'on' if state else 'off'}.")
        except Exception as e: print(f"Error: {e}")

    def repeat(self, state):
        try:
            self._execute_safe(self.client.repeat, state)
            print(f"Set repeat mode to {'on' if state else 'off'}.")
        except Exception as e: print(f"Error: {e}")
        
    def costume(self, state):
        try:
            self._execute_safe(self.client.consume, state)
            print(f"Set consume mode to {'on' if state else 'off'}.")
        except Exception as e: print(f"Error: {e}")    

    def replay_gain_mode(self, mode):
        try:
            self._execute_safe(self.client.replay_gain_mode, mode)
            print(f"Set replay gain mode to {mode}.")
        except Exception as e: print(f"Error: {e}")

    def seek(self, songpos, time):
        try:
            self._execute_safe(self.client.seek, songpos, time)
            print(f"Seeking to {time}s in song at position {songpos}.")
        except Exception as e: print(f"Error: {e}")

    def seekid(self, songid, time):
        try:
            self._execute_safe(self.client.seekid, songid, time)
            print(f"Seeking to {time}s in song with ID {songid}.")
        except Exception as e: print(f"Error: {e}")

    def seekcur(self, time):
        try:
            self._execute_safe(self.client.seekcur, time)
            print(f"Seeking to {time}s in current song.")
        except Exception as e: print(f"Error: {e}")

    def get_current_song_duration(self):
        """Gets the total duration of the currently playing song."""
        try:
            status = self.get_status()
            if status and 'duration' in status:
                return status['duration']
            return None
        except Exception as e:
            print(f"Error getting song duration: {e}")
            return None

    def get_current_song_elapsed_time(self):
        """Gets the elapsed time of the currently playing song."""
        try:
            status = self.get_status()
            if status and 'elapsed' in status:
                return status['elapsed']
            return None
        except Exception as e:
            print(f"Error getting elapsed time: {e}")
            return None

    # --- Playlist / Queue Operations ---

    def queue_load_radiostreams(self, streams_dict):
        try:
            if not self.is_connected: self.connect()
            self.client.clear()
            for url in streams_dict.values():
                self.client.add(url)
            print(f"Loaded {len(streams_dict)} radio streams.")
        except (MPDConnectionError, OSError):
            self.is_connected = False
            self.connect()
            # Retry logic could be added here if needed, but complex for multi-step ops
            print("Reconnected, please try loading streams again.")

    def queue_add_song(self, path):
        try:
            self._execute_safe(self.client.add, path)
            print(f"Added '{path}' to the playlist.")
        except Exception as e:
            print(f"Error adding song: {e}")
    def queue_add_songid(self, uri, position=None):
        try:
            if position is None:
                song_id = self._execute_safe(self.client.addid, uri)
            else:
                song_id = self._execute_safe(self.client.addid, uri, position)
            return song_id
        except Exception as e:
            print(f"Error: {e}")
            return None
            
    def add_tagid(self, songid, tag, value):
        """Adds a tag to a song."""
        try:
            self._execute_safe(self.client.addtagid, songid, tag, value)
            print(f"Added tag '{tag}: {value}' to songid {songid}")
        except Exception as e:
            print(f"Error adding tag to songid {songid}: {e}")
    

    def queue_add_folder(self, music_folder):
        try:
            self._execute_safe(self.client.add, music_folder)
            print(f"Added all files from '{music_folder}' to the playlist.")
        except Exception as e:
            print(f"Error adding folder: {e}")
            
    def queue_delete(self, songpos):
        #Deletes a song, or a range of songs, from the queue based on the song’s position in queue.
        #A range can be specified by passing a tuple.
        try:
            self._execute_safe(self.client.delete, songpos)
        except Exception as e: print(f"Error: {e}")
    def queue_deleteid(self, songid):
        #Deletes the song SONGID from the queue.
        try:
            self._execute_safe(self.client.deleteid, songid)
        except Exception as e: print(f"Error: {e}")
                
    def queue_current_song(self):
        try:
            current_song = self._execute_safe(self.client.currentsong)
            return current_song
        except Exception as e:
            print(f"Error: {e}")
            return None

    def queue_get_songs(self):
        try:
            return self._execute_safe(self.client.playlistinfo)
        except Exception as e:
            print(f"Error: {e}")
            return []

    def queue_get_songsid(self):
        try:
            return self._execute_safe(self.client.playlistid)
        except Exception as e:
            print(f"Error: {e}")
            return []

    def queue_clearsongs(self):
        try:
            self._execute_safe(self.client.clear)
            print("Queue songs cleared.")
        except Exception as e:
            print(f"Error: {e}")

    # --- Stored Playlists ---

    def get_playlist_List(self):
        #list all stored playlists
        try:
            return self._execute_safe(self.client.listplaylists)
        except Exception as e:
            print(f"Error: {e}")
            return []
    def playlist_renamepl(self, pi_plname, new_pi_plname):
        try:
            self._execute_safe(self.client.rename, pi_plname, new_pi_plname)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        
    def playlist_rmpl(self, pi_plname):
        try:
            self._execute_safe(self.client.rm, pi_plname)
        except Exception as e:
            print(f"Error: {e}")
            raise e
            
        
    def queue_saveto_playlist(self, pi_plname):
        try:
            self._execute_safe(self.client.save, pi_plname)
            print(f"Playlist saved as '{pi_plname}'")
        except Exception as e:
            print(f"Error: {e}")

    def queue_loadfrom_playlist(self, pi_plname):
        try:
            self._execute_safe(self.client.load, pi_plname)
            print(f"Playlist '{pi_plname}' loading")      
        except Exception as e:
            print(f"Error: {e}")
                   
    def playlist_songs(self, pi_plname):
        try:
            return self._execute_safe(self.client.listplaylist, pi_plname)
        except Exception as e:
            print(f"Error: {e}")
            return []       
    def playlist_songsinfo(self, pi_plname):
        try:
            return self._execute_safe(self.client.listplaylistinfo, pi_plname)
        except Exception as e:
            print(f"Error: {e}")
            return []


    def playlist_deletesong(self, pi_plname, songpos):
        try:
            self._execute_safe(self.client.playlistdelete, pi_plname, songpos)
        except Exception as e:
            print(f"Error: {e}")
            raise e


    def playlist_clearsongs(self, pi_plname):
        try:
            self._execute_safe(self.client.playlistclear, pi_plname)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        
    def playlist_add_song(self, pi_plname, uri):
        try:
            # Check if the playlist exists
            playlists = self._execute_safe(self.client.listplaylists)
            playlist_exists = any(p['playlist'] == pi_plname for p in playlists)

            if not playlist_exists:
                # If playlist doesn't exist, create it (playlistadd does this implicitly but good to be explicit)
                # It's better to add a dummy song and then remove it to truly "create" an empty playlist,
                # as playlistadd will just create it when the first song is added.
                # However, for simply adding, playlistadd handles creation.
                print(f"Playlist '{pi_plname}' does not exist. It will be created.")

            # Get current songs in the playlist to check for duplicates
            current_playlist_songs = self._execute_safe(self.client.listplaylist, pi_plname)
            
            # Check if the song URI is already in the playlist
            if uri in current_playlist_songs:
                print(f"Song '{uri}' is already in playlist '{pi_plname}'. Not adding duplicate.")
                return {"message": f"Song '{uri}' is already in playlist '{pi_plname}'. Not adding duplicate."}
            
            # If not a duplicate, add the song
            self._execute_safe(self.client.playlistadd, pi_plname, uri)
            print(f"URI '{uri}' added to playlist '{pi_plname}'.")
            return {"message": f"URI '{uri}' added to playlist '{pi_plname}'."}
        except Exception as e:
            print(f"Error adding URI to playlist: {e}")
            raise e 
               
    def playlist_add_folder(self, pi_plname, foldername):
        try:
            files = self._list_music_files_in_folder(foldername)
            if not files:
                message = f"No music files found in folder '{foldername}'."
                print(message)
                return {"message": message}
            for file_path_mpd in files:
                self._execute_safe(self.client.playlistadd, pi_plname, file_path_mpd)
            message = f"Added all files from '{foldername}' to playlist '{pi_plname}'."
            print(message)
            return {"message": message}
        except Exception as e:
            error_message = f"Error adding folder to playlist: {e}"
            print(error_message)
            return {"error": error_message}

    def browse_directory(self, path):
        """Browses a directory in the MPD music folder."""
        try:
            items = self._execute_safe(self.client.lsinfo, path)
            results = []
            for item in items:
                if 'directory' in item:
                    name = os.path.basename(item['directory'])
                    results.append({'name': name, 'type': 'directory', 'path': item['directory']})
                elif 'file' in item:
                    name = os.path.basename(item['file'])
                    results.append({'name': name, 'type': 'file', 'path': item['file']})
            return results
        except Exception as e:
            print(f"Error browsing directory: {e}")
            return []

    def pi_save_selection_to_playlist(self, playlist_name: str, songs: list):
        """
        Creates a new playlist from a list of selected songs.
        If the playlist already exists, it will be overwritten.
        """
        try:
            # Check if a playlist with the same name exists and remove it.
            playlists = self._execute_safe(self.client.listplaylists)
            if any(p['playlist'] == playlist_name for p in playlists):
                self._execute_safe(self.client.rm, playlist_name)
                print(f"Removed existing playlist '{playlist_name}'.")

            # Add each song to the new playlist.
            for song_uri in songs:
                self._execute_safe(self.client.playlistadd, playlist_name, song_uri)
            
            print(f"Successfully created playlist '{playlist_name}' with {len(songs)} songs.")
            return {"message": f"Playlist '{playlist_name}' created successfully."}

        except MPDCommandError as e:
            error_message = f"MPD command error while saving selection to playlist: {e}"
            print(error_message)
            raise e  # Re-raise to be caught by FastAPI handler
        except Exception as e:
            error_message = f"An unexpected error occurred while saving selection: {e}"
            print(error_message)
            raise e

    def create_playlist_if_not_exists(self, playlist_name, folder_name):
        """
        Checks if a playlist exists. If not, creates it from a folder.
        """
        playlists = self.get_playlist_List()
        if any(p['playlist'] == playlist_name for p in playlists):
            print(f"Playlist '{playlist_name}' already exists.")
            return

        print(f"Playlist '{playlist_name}' not found. Creating it from folder '{folder_name}'.")
        self.playlist_add_folder(playlist_name, folder_name)


    def _list_music_files_in_folder(self, foldername):
        """
        Scans a directory for music files and returns their paths relative to the MPD music root.
        """
        music_extensions = ['.mp3', '.flac', '.ogg', '.wav', '.aac']
        
        full_folder_path = os.path.join(self.music_base_path, foldername)

        if not os.path.isdir(full_folder_path):
            print(f"Error: Directory not found at '{full_folder_path}'")
            return []

        music_files = []
        for root, _, files in os.walk(full_folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in music_extensions):
                    full_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_file_path, self.music_base_path)
                    music_files.append(str(Path(relative_path)))

        return music_files