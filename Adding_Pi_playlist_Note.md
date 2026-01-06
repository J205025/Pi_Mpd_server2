Please build a  pi_playlist.vue that similiar to pc_playlist.vue. But this time, I will build the pi_playlist.vue to manage the stored playlist in mpd.service. And I already build the required APIs in backend main.py. Please build this pi_playlist.vue from API provided by main.py. If It needs other APIs in main.py , and functions in mpd_controller.py. Please refer to https://python-mpd2.readthedocs.io/en/latest/topics/commands.html ,  section "Stored playlists". 

In pc_playlist.vue pc_getFiles is changed to new name pi_getFiles in pi_playlist.vue,and it may use pi_playlist_add_folder/{pi_plname}/{foldername} and /pi_playlist_songs/{pi_plname} to show the songs on pc_playlist.vue when user  click the button 搜尋資料夾 and shows the songd in "Generated Files:" section. 

I also explain the some required APIs in main.py , as follows:
/pi_get_playlists_List is to list all the stored playlist name in mpd.
/pi_playlist_renamepl/{old_name}/{new_name} is to change the stored playlist name in mpd.
/pi_playlist_rmpl/{pi_plname} is to remove the specified playlist  in stored playlist in mpd.
/pi_playlist_songs/{pi_plname}  is to show the Songs in specified stored playlist in mpd.
/pi_playlist_songsinfo/{pi_plname}  is to show the Songs info in specified stored playlist in mpd.  
/pi_playlist_deletesong/{pi_plname}/{songpos}  is to delete the song at songpod in stored playlist in mpd.
/pi_playlist_clearsongs/{pi_plname}  is to clear song in the specified playlist name in mpd
/pi_playlist_adduri/{pi_plname}/{uri}  is to add a song to specified playlist in mpd
/pi_playlist_add_folder/{pi_plname}/{foldername} is to add the file in folder and save to a playlistname.


--------------------------------------------------------
Please build a  piplayer.vue that similiar to pcplayer.vue. But this time, pi_playlist.vue is to play the song by using mpd.service. 
Beacuse, the mpd player has current playing playlist(queue), and stored playlist, 
please add another queue seection to manage the current playing playlist.
The current playing queue can be loaded from stored playlist, ie, from this api  /pi_queue_loadfrom_playlist/{pi_plname}. 
And, the stored playlist section  is similiar to  選擇歌單: section in pcplayer.vue to view the stroed playlist. 

I have build some API in main.py.
/pi_mpd_status
/pi_get_current_song_duration
/pi_get_current_song_elapsed_time
/pi_play
/pi_playid/{song_id}
/pi_pause
/pi_stop
/pi_next
/pi_prev
/pi_setvol/{volume}
/pi_playmode 
/pi_queue_songs/
/pi_queue_songsid/
/pi_queue_clearsongs/
/pi_queue_add_song
/pi_queue_add_folder/{foldername}
/pi_queue_current_song
/pi_queue_loadfrom_playlist/{pi_plname}
/pi_queue_saveto_playlist/{pi_plname}

If It needs other APIs in main.py , and functions in mpd_controller.py. Please refer to https://python-mpd2.readthedocs.io/en/latest/topics/commands.html

