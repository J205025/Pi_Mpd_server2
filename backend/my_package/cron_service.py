# my_package/cron_service.py
import os
from crontab import CronTab
from .mpd_controller import MPDClientController
from typing import Optional, List # Import List and Optional

# It's better to get the python path dynamically
python_executable = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".venv/bin/python")
script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cron_task.py")
CRON_COMMENT = "mpd-player-cron"

def get_cron_jobs():
    """
    Lists all cron jobs managed by this application.
    """
    cron = CronTab(user=True)
    jobs = []
    for job in cron:
        if job.comment == CRON_COMMENT:
            # job.slices returns a tuple (minute, hour, day_of_month, month, day_of_week)
            # We want to reconstruct the cron string from it
            # The day_of_month and month are always '*' in our use case
            schedule_parts = [
                str(job.minute),
                str(job.hour),
                str(job.dom), # day_of_month
                str(job.month), # month
                str(job.dow)  # day_of_week
            ]
            jobs.append({
                "schedule": ' '.join(schedule_parts),
                "command": job.command,
                "comment": job.comment
            })
    return jobs

def add_cron_job(hour: int, minute: int, day_of_week: Optional[List[int]] = None):
    """
    Adds a new cron job to play the '定期播放' playlist.
    """
    cron = CronTab(user=True)
    
    # Create playlist before adding cron job
    mpd_controller = MPDClientController()
    mpd_controller.connect()
    if mpd_controller.is_connected:
        mpd_controller.create_playlist_if_not_exists("定期播放", "定期播放")
        mpd_controller.disconnect()
    else:
        raise Exception("MPD is not connected.")

    command = f'{python_executable} {script_path}'
    
    # Remove existing job before adding a new one to avoid duplicates
    remove_cron_job()
    
    # Determine day of week setting
    if day_of_week is None or len(day_of_week) == 0 or len(day_of_week) == 7:
        dow_cron_value = '*' # Every day
    else:
        dow_cron_value = ','.join(map(str, sorted(day_of_week))) # Specific days

    job = cron.new(command=command, comment=CRON_COMMENT)
    job.setall(minute, hour, '*', '*', dow_cron_value)
    cron.write()
    return {"message": f"Cron job scheduled at {hour:02d}:{minute:02d} on days {dow_cron_value}."}

def remove_cron_job():
    """
    Removes all cron jobs managed by this application.
    """
    cron = CronTab(user=True)
    initial_len = len(cron)
    
    for job in cron:
        if job.comment == CRON_COMMENT:
            cron.remove(job)
            
    if len(cron) < initial_len:
        cron.write()
        return {"message": "Cron job removed."}
    else:
        return {"message": "No cron job found to remove."}



