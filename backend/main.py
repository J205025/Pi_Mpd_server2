# main.py
# This script creates a FastAPI application to expose API endpoints
# for controlling the Music Player Daemon (MPD).
import os, io, json, uvicorn, subprocess, asyncio

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import timedelta
from pathlib import Path
from contextlib import asynccontextmanager
from PIL import Image
from pydantic import BaseModel

from my_package.mpd_controller import MPDClientController
from my_package.database import get_db, SessionLocal, Base, engine
from my_package.models import User, UserPlaylist
from my_package.schemas import (
    UserCreate, UserResponse, Token, UserPlaylistCreate, UserPlaylistResponse,
    PlaylistPayload, PlaylistsListResponse, UserPasswordChange, Settings, SongRequest
)
from my_package.auth import (
get_password_hash, verify_password, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
)
import my_package.cron_service as cron_service

# ----------------------------------------------
music_Basefolder = "/home/ubuntu/Music/"
music_Type = [] # Will be populated at startup
#-----------------------------------------------
pi_ALLFILES = [] 
pi_Playlist_List = []  
pi_playlist_files = []
pi_IndexMax = 1
pi_Index = 0
pi_Playing = None
pi_Playmode = None
pi_RadioNo = None
pi_Volume = 1
pi_Mute = False
pi_Playrate = 1
pi_Duration = 0
cron_Status =  False
cron_Hour = '00'
cron_Min = '00'
cron_pi_Index = 1
pc_ALLFILES = []
pc_Playlist_List = [] 
pc_Playlist_files = []
pc_Indexmax = 1

# Initialize the MPD client controller globally
mpd_player = MPDClientController(music_base_path=music_Basefolder)

MPD_PLAYMODE = ["repeat", "random", "single", "consume"]

class CronJobPayload(BaseModel):
    hour: int
    minute: int
    day_of_week: Optional[List[int]] = None

class StreamRequest(BaseModel):
    stream_url: str
    title: str
    artist: str

class PlaylistDeleteSongPayload(BaseModel):
    pi_plname: str
    songpos: int

class YouTubeAddPayload(BaseModel):
    playlist_name: str
    youtube_url: str

class SaveSelectionPayload(BaseModel):
    playlist_name: str
    songs: List[str]


# Generate filespath base from music_Basefolder
def genFilelist(subfolder):
    global pc_Indexmax
    global music_Basefolder 
    songs = []; 
    for path, subdirs, files in os.walk(music_Basefolder + subfolder, followlinks=True):
        path = path[len(music_Basefolder):]
        if path.startswith('/'):
            path = path[1:]
        path = path+"/"
        if path == '/':
            path = ''
        files = [path + file for file in files]
        songs = songs + files; 
    songs = [ f for f in songs if f.lower().endswith(('.mp3', '.flac'))]
    songs.sort()
    return songs

# --- Application Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global music_Type
    """
    Handles application startup and shutdown events.
    """
    print("Application startup...")

    # --- START: Dynamically find music types ---
    print(f"Scanning for music types in: {music_Basefolder}")
    base_path = Path(music_Basefolder)
    if base_path.is_dir():
        subfolders = [item.name for item in base_path.iterdir() if item.is_dir()]
        music_Type.extend(sorted(subfolders)) 
        print(f"✅ Found music types: {music_Type}")
    else:
        print(f"⚠️  Warning: Music base folder not found at '{music_Basefolder}'")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Connect to MPD
    # Note: mpd_controller now handles connection errors gracefully, 
    # so even if this initial connect fails, the app will continue.
    mpd_player.connect()

    if mpd_player.is_connected:
        print("MPD is connected Updating MPD database...")
        mpd_player.update()
        
        # Create playlists based on folder names
        #for folder_name in music_Type:
        #    print(f"  -> Processing and creating playlist for: '{folder_name}'")
        #    mpd_player.queue_clearsongs()
        #    mpd_player.queue_add_folder(folder_name)
        #    mpd_player.queue_saveto_playlist(folder_name)
        
        #mpd_player.queue_clearsongs()
        #print("✅ Playlist creation complete.")
    else:
        print("⚠️  MPD not connected at startup. Features will activate when MPD becomes available.")

    try:
        yield
    finally:
        print("Application shutdown...")
        mpd_player.disconnect()
  
# --- FastAPI App Setup ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]
app = FastAPI(lifespan=lifespan,
    title="MPD Player API",
    description="A Player with Music Player Daemon (MPD).",
    version="1.0.0"
)

# Path to your built Nuxt.js application
NUXT_DIST_PATH = Path("../frontend/.output/public")

if not NUXT_DIST_PATH.exists():
    # You might want to make this a warning instead of a crash for dev purposes
    print(f"WARNING: Nuxt build not found at {NUXT_DIST_PATH}.")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="backend_static")
if NUXT_DIST_PATH.exists():
    app.mount("/_nuxt", StaticFiles(directory=NUXT_DIST_PATH / "_nuxt"), name="nuxt_assets")
    app.mount("/images", StaticFiles(directory=NUXT_DIST_PATH / "images"), name="nuxt_images")
    app.mount("/app", StaticFiles(directory=NUXT_DIST_PATH, html=True), name="nuxt_app")
    
app.mount("/music", StaticFiles(directory="/home/ubuntu/Music"), name="music_files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

@app.get("/")
async def root():
    index_file = NUXT_DIST_PATH / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        return HTMLResponse("<h1>Welcome! Nuxt app not found (Build frontend first).</h1>")

@app.get("/_payload.json")
async def serve_payload():
    payload_file = NUXT_DIST_PATH / "_payload.json"
    if payload_file.exists():
        return FileResponse(payload_file, media_type="application/json")
    return JSONResponse({})

@app.get("/{path:path}/_payload.json")
async def serve_dynamic_payload(path: str):
    payload_file = NUXT_DIST_PATH / path / "_payload.json"
    if payload_file.exists():
        return FileResponse(payload_file, media_type="application/json")
    main_payload = NUXT_DIST_PATH / "_payload.json"
    if main_payload.exists():
        return FileResponse(main_payload, media_type="application/json")
    return JSONResponse({})

# --- State Endpoint ---

@app.post("/pi_mpd_connect")
async def pi_mpd_connect():
    """Forces a reconnection attempt."""
    try:
        mpd_player.connect()
        if mpd_player.is_connected:
            return {"message": "Successfully connected to MPD."}
        else:
             raise HTTPException(status_code=503, detail="Failed to connect to MPD server.")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Could not connect to MPD: {e}")

@app.post("/pi_mpd_update")
async def pi_mpd_update():
    """Triggers an update of the MPD database."""
    try:
        mpd_player.update()
        return {"message": "MPD database update initiated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update MPD database: {e}")

@app.get("/pi_mpd_status")
async def get_pi_status():
    """Returns the current status of the MPD player."""
    # get_status() handles reconnection internally now
    status = mpd_player.get_status()
    if status is None:
        # If still None after auto-reconnect, then MPD is truly down
        raise HTTPException(status_code=503, detail="MPD is not connected or unavailable")
    return status

@app.get("/pi_get_current_song_duration")
async def get_pi_current_song_duration():
    """Returns the total duration of the currently playing song."""
    duration = mpd_player.get_current_song_duration()
    if duration is None:
        raise HTTPException(status_code=404, detail="Could not retrieve song duration.")
    return {"duration": duration}

@app.get("/pi_get_current_song_elapsed_time")
async def get_pi_current_song_elapsed_time():
    """Returns the elapsed time of the currently playing song."""
    elapsed = mpd_player.get_current_song_elapsed_time()
    if elapsed is None:
        raise HTTPException(status_code=404, detail="Could not retrieve elapsed time.")
    return {"elapsed": elapsed}

### Pi MPD Control APIs
@app.post("/pi_play")
async def pi_play():
    mpd_player.play()
    return {"message": "Playback started."}
    
@app.post("/pi_playid/{song_id}")
async def pi_playid(song_id: str):
    try:
        mpd_player.client.playid(song_id)
        return {"message": f"Playing song with id {song_id}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.post("/pi_pause")
async def pi_pause():
    mpd_player.pause()
    return {"message": "Playback paused/unpaused."}

@app.post("/pi_stop")
async def pi_stop():
    mpd_player.stop()
    return {"message": "Playback stopped."}

@app.post("/pi_next")
async def pi_next():
    mpd_player.next()
    return {"message": "Skipped to the next song."}

@app.post("/pi_prev")
async def pi_prev():
    mpd_player.prev()
    return {"message": "Skipped to the previous song."}

@app.put("/pi_setvol/{volume}")
async def pi_setvol(volume: int):
    mpd_player.setvol(volume)
    return {"message": f"Volume set to {volume}."}

@app.put("/pi_seekcur/{time}")
async def pi_seekcur(time: float):
    mpd_player.seekcur(time)
    return {"message": f"Seeking to {time}s in current song."}

@app.put("/pi_playmode")
async def pi_playmode(repeat: Optional[bool] = None, random: Optional[bool] = None, single: Optional[bool] = None, costume: Optional[bool] = None):
    # We can rely on the controller or direct client access (which is wrapped in controller now ideally)
    if repeat is not None: mpd_player.repeat(1 if repeat else 0)
    if random is not None: mpd_player.random(1 if random else 0)
    if single is not None: mpd_player.single(1 if single else 0)
    if costume is not None: mpd_player.costume(1 if costume else 0)
    return {"message": "Play mode updated."}

@app.post("/pi_add_and_play_stream")
async def pi_add_and_play_stream(payload: StreamRequest, current_user: User = Depends(get_current_user)):
    try:
        mpd_player.queue_clearsongs()
        song_id = mpd_player.queue_add_songid(payload.stream_url)
        if song_id:
            mpd_player.add_tagid(song_id, "title", payload.title)
            mpd_player.add_tagid(song_id, "artist", payload.artist)
        mpd_player.play()
        return {"status": "success", "message": "Stream added and is now playing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to play stream: {e}")

@app.get("/pi_mpd_browse/")
@app.get("/pi_mpd_browse/{path:path}")
async def pi_mpd_browse(path: Optional[str] = None):
    """Browses the MPD music directory."""
    browse_path = path if path else ""
    try:
        return mpd_player.browse_directory(browse_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to browse directory: {e}")

### Pi MPD Queue APIs
# Define the queue OUTSIDE the functions
#pi_queue_songs = []
@app.get("/pi_queue_songs")
async def pi_queue_files():
    return mpd_player.queue_get_songs()

@app.get("/pi_queue_songsid")
async def pi_queue_filesid():
    return mpd_player.queue_get_songsid()
@app.delete("/pi_queue_clearsongs")
async def pi_queue_clearsongs():
    return mpd_player.queue_clearsongs()

@app.post("/pi_queue_add_song")
async def pi_queue_add_song(song: SongRequest):
    mpd_player.queue_add_song(song.path)
    return {"message": f"Song '{song.path}' added to the queue."}

@app.get("/pi_queue_add_folder/{foldername:path}")  # <--- Note the :path here
async def pi_gen_playlist(foldername:str):
    mpd_player.queue_add_folder(foldername)
    return {"message": f"Folder {foldername} added."}

@app.get("/pi_queue_current_song")
async def pi_queue_current_song():
    current_song = mpd_player.queue_current_song()
    if current_song is None:
        return {"message": "No song is currently playing."}
    return current_song
    
@app.get("/pi_queue_loadfrom_playlist/{pi_plname}")
async def pi_load_playlist_to_queue(pi_plname:str):
    mpd_player.queue_loadfrom_playlist(pi_plname)
    return {"message": f"Loading '{pi_plname}'."}
    
@app.get("/pi_queue_saveto_playlist/{pi_plname}")
async def pi_queue_save_to_playlist(pi_plname:str):
    mpd_player.queue_saveto_playlist(pi_plname)
    return {"message": "Playlist saved."}


    
### Pi MPD Playlist APIs    
@app.get("/pi_get_playlists_List")
async def pi_get_playlist_List():
    return mpd_player.get_playlist_List()

@app.put("/pi_playlist_renamepl/{old_name}/{new_name}")
async def pi_playlist_renamepl(old_name: str, new_name: str):
    try:
        mpd_player.playlist_renamepl(old_name, new_name)
        return {"message": f"Playlist '{old_name}' renamed to '{new_name}' successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming playlist: {e}")

@app.delete("/pi_playlist_rmpl/{pi_plname}")
async def pi_playlist_rmpl(pi_plname: str):
    try:
        mpd_player.playlist_rmpl(pi_plname)
        return {"message": f"Playlist '{pi_plname}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting playlist: {e}")
    
@app.get("/pi_playlist_songs/{pi_plname}")
async def pi_playlist_songs(pi_plname: str):
    return mpd_player.playlist_songs(pi_plname)

@app.get("/pi_playlist_songsinfo/{pi_plname}")
async def pi_playlist_songsinfo(pi_plname: str):
    return mpd_player.playlist_songsinfo(pi_plname)

@app.delete("/pi_playlist_deletesong/{pi_plname}/{songpos}")
async def pi_playlist_deletesong(pi_plname: str, songpos: int):
    try:
        # MPD is 0-indexed, so we might need to adjust if the user provides a 1-based index.
        # Assuming the user provides a 0-based index for now.
        mpd_player.playlist_deletesong(pi_plname, songpos)
        return {"message": f"Song at position {songpos} deleted from playlist '{pi_plname}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting song from playlist: {e}")

@app.post("/pi_playlistdeletesong")
async def pi_playlistdeletesong_post(payload: PlaylistDeleteSongPayload):
    try:
        mpd_player.playlist_deletesong(payload.pi_plname, payload.songpos)
        return {"message": f"Song at position {payload.songpos} deleted from playlist '{payload.pi_plname}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting song from playlist: {e}")

@app.delete("/pi_playlist_clearsongs/{pi_plname}")
async def pi_playlist_clearsongs(pi_plname: str):
    try:
        mpd_player.playlist_clearsongs(pi_plname)
        return {"message": f"Playlist '{pi_plname}' cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing playlist: {e}")

@app.post("/pi_playlist_adduri/{pi_plname}/{uri:path}")
async def pi_playlist_adduri(pi_plname: str, uri: str):
    try:
        mpd_player.playlist_add_song(pi_plname, uri)
        return {"message": f"URI '{uri}' added to playlist '{pi_plname}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding URI to playlist: {e}")

@app.post("/pi_playlist_add_folder/{pi_plname}/{foldername:path}")
async def pi_playlist_add_folder(pi_plname: str, foldername: str):
    try:
        folder_for_mpd = foldername
        if foldername == 'ALL_FILES':
            folder_for_mpd = '.'
        result = mpd_player.playlist_add_folder(pi_plname, folder_for_mpd)
        if "error" in result:
             raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding folder to playlist: {e}")
@app.post("/playlist/add_youtube_song")
async def add_youtube_song(payload: YouTubeAddPayload):
    try:
        # Use yt-dlp to get the direct audio URL
        process = await asyncio.create_subprocess_exec(
            'yt-dlp',
            '-f', 'bestaudio/best',
            '--get-url',
            '--no-playlist',  # <--- ADD THIS LINE HERE
            payload.youtube_url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"yt-dlp error: {stderr.decode()}")

        stream_url = stdout.decode().strip()

        # Add the stream URL to the playlist
        mpd_player.playlist_add_song(payload.playlist_name, stream_url)

        return {"message": f"Successfully added video from {payload.youtube_url} to playlist {payload.playlist_name}."}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="yt-dlp is not installed or not in PATH.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing YouTube URL: {e}")

@app.post("/pi_playlist/save_selection")
async def pi_playlist_save_selection(payload: SaveSelectionPayload):
    try:
        result = mpd_player.pi_save_selection_to_playlist(payload.playlist_name, payload.songs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving selection to playlist: {e}")

### Cron Job APIs
@app.get("/api/cron")
async def get_cron_jobs():
    return cron_service.get_cron_jobs()

@app.post("/api/cron")
async def add_cron_job(payload: CronJobPayload):
    try:
        return cron_service.add_cron_job(payload.hour, payload.minute, payload.day_of_week)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cron")
async def remove_cron_job():
    return cron_service.remove_cron_job()

### PC Player API
@app.get("/pc_get_allfiles")
async def pc_get_allfiles(
    current_user: User = Depends(get_current_user)
):
    fileslist = genFilelist('')
    return fileslist

@app.get("/pc_get_playlist_List", response_model=PlaylistsListResponse)
async def pc_get_playlists_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist_names_tuples = db.query(UserPlaylist.playlist_name).filter(UserPlaylist.user_id == current_user.id).all()
    playlist_names = [name for (name,) in playlist_names_tuples]
    return {"names": playlist_names}

@app.get("/pc_playlist_files/{pc_plname}")
async def pc_playlist_files(
    pc_plname :str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_playlist = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    if user_playlist:
        return json.loads(user_playlist.playlist_data)
    return []

@app.post("/pc_playlist_saveto_list/{pc_plname}")
async def pc_playlist_saveto_list(
    pc_plname: str,
    payload: PlaylistPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_playlist = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    playlist_data_json = json.dumps(payload.songs)

    if user_playlist:
        user_playlist.playlist_data = playlist_data_json
        db.commit()
        db.refresh(user_playlist)
        return {"message": f"Playlist '{pc_plname}' updated successfully"}
    else:
        new_playlist = UserPlaylist(
            user_id=current_user.id,
            playlist_name=pc_plname,
            playlist_data=playlist_data_json
        )
        db.add(new_playlist)
        db.commit()
        db.refresh(new_playlist)
        return {"message": f"Playlist '{pc_plname}' created successfully"}

@app.delete("/pc_playlist_rmpl/{pc_plname}")
async def pc_playlist_rmpl(
    pc_plname: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist_to_delete = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    if not playlist_to_delete:
        raise HTTPException(status_code=404, detail=f"Playlist '{pc_plname}' not found")

    db.delete(playlist_to_delete)
    db.commit()
    return {"message": f"Playlist '{pc_plname}' deleted successfully"}

@app.get("/pc_browse/")
@app.get("/pc_browse/{path:path}")
async def pc_browse(
    path: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Browses the PC music directory."""
    base_path = Path(music_Basefolder).resolve()
    browse_path = base_path

    if path:
        browse_path = (base_path / path).resolve()

    # Security check: Ensure the resolved path is within the base music folder.
    # This prevents directory traversal attacks (e.g., path = "../..")
    try:
        if not browse_path.is_relative_to(base_path):
            raise HTTPException(status_code=400, detail="Invalid path")
    except ValueError:
        # This can happen if the paths are on different drives in Windows,
        # or other complex scenarios. For our case, it's an invalid path.
        raise HTTPException(status_code=400, detail="Invalid path")

    if not browse_path.exists() or not browse_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    items = []
    for item in sorted(browse_path.iterdir()):
        try:
            item_path_str = str(item.relative_to(base_path))
        except ValueError:
            continue
            
        if item.is_dir():
            items.append({"type": "directory", "path": item_path_str, "name": item.name})
        else:
            if item.suffix.lower() in ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac']:
                items.append({"type": "file", "path": item_path_str, "name": item.name})
    return items

@app.get("/pc_gen_fileslist/{foldername}")
async def pc_gen_fileslist(
    foldername :str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    path_to_scan = foldername
    if foldername == 'ALL_FILES':
        path_to_scan = '.'
            
    folderpath = path_to_scan.replace(" ", "/")
    fileslist = genFilelist(folderpath)
    return fileslist

# --- User Management ---
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    DESIGNATED_CODE = "Happy"
    if user.code != DESIGNATED_CODE:
        raise HTTPException(status_code=400, detail="Invalid registration code")
    
    username_capitalized = user.username.upper()
    db_user = db.query(User).filter(User.username == username_capitalized).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    default_settings = {
        "show_lyrics": True,
        "show_radio_card": True,
        "sleeping_time": 20,
        "spare_setting1": True,
        "spare_setting2": True,
        "id3tagDisplaytype": False
    }
    db_user = User(
        username=username_capitalized,
        hashed_password=hashed_password,
        settings=json.dumps(default_settings)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    new_playlist = UserPlaylist(
        user_id=db_user.id,
        playlist_name="我的最愛",
        playlist_data=json.dumps([])
    )
    db.add(new_playlist)
    db.commit()

    settings_dict = json.loads(db_user.settings) if db_user.settings else None
    return UserResponse(id=db_user.id, username=db_user.username, settings=settings_dict)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username_capitalized = form_data.username.upper()
    user = db.query(User).filter(User.username == username_capitalized).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    settings_dict = json.loads(current_user.settings) if current_user.settings else None
    return UserResponse(id=current_user.id, username=current_user.username, settings=settings_dict)

@app.put("/users/me/settings")
async def update_user_settings(
    settings: Settings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.settings = json.dumps(settings.dict())
    db.commit()
    db.refresh(current_user)
    return {"message": "Settings updated successfully"}

@app.put("/users/password")
async def change_password(
    password_data: UserPasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    if len(password_data.new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 6 characters long")
    
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(current_user)
    return {"message": "Password changed successfully"}



@app.post("/upload_user_picture")
async def upload_user_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    save_path = Path(f"../frontend/public/images/user_picture/{current_user.username}.jpg")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        image_data = await file.read()
        with Image.open(io.BytesIO(image_data)) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(save_path, 'jpeg')
        return {"message": "Picture uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading picture: {e}")

@app.get("/api/wallpaper-images")
async def get_wallpaper_images():
    image_dir = NUXT_DIST_PATH / "images" / "home_picture"   
    if not image_dir.is_dir():
        # Fallback to local dev path if dist doesn't exist
        image_dir = Path("../frontend/public/images/home_picture/")
        if not image_dir.is_dir():
            return []
    
    images = [f"/images/home_picture/{p.name}" for p in image_dir.iterdir() if p.is_file()]
    return images

@app.post("/download_podcast")
async def download_podcast(current_user: User = Depends(get_current_user)):
    try:
        python_executable = os.path.join(os.path.dirname(__file__), ".venv/bin/python")
        script_path = os.path.join(os.path.dirname(__file__), "podcastdl_task.py")
        await asyncio.create_subprocess_exec(python_executable, script_path)
        return {"message": "Podcast download started in the background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Catch-all route
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    if full_path.startswith(("api/", "_nuxt/", "music/", "static/", "app/")):
        raise HTTPException(status_code=404, detail="Not found")
    if full_path.endswith("_payload.json"):
        raise HTTPException(status_code=404, detail="Payload not found")
    if "." in full_path.split("/")[-1] and not full_path.endswith(".html"):
        raise HTTPException(status_code=404, detail="Not found")
    
    index_file = NUXT_DIST_PATH / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)