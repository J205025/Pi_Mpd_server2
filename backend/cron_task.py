# backend/cron_task.py
import sys
import os

# Add the project's backend directory to the Python path
# This is necessary so that the script can find the 'my_package' module
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from my_package.mpd_controller import MPDClientController

def play_playlist():
    """
    Connects to MPD, loads the '定期播放' playlist, and starts playback.
    """
    print("Executing cron task: play_playlist")
    mpd_controller = MPDClientController()
    mpd_controller.connect()

    if not mpd_controller.is_connected:
        print("Cron task failed: Could not connect to MPD.")
        return

    try:
        print("Clearing current queue.")
        mpd_controller.queue_clearsongs()
        print("Loading playlist: 定期播放")
        mpd_controller.queue_loadfrom_playlist("定期播放")
        print("Starting playback.")
        mpd_controller.play()
        print("Cron task completed successfully.")
    except Exception as e:
        print(f"An error occurred during the cron task: {e}")
    finally:
        mpd_controller.disconnect()
        print("Disconnected from MPD.")

if __name__ == "__main__":
    play_playlist()
