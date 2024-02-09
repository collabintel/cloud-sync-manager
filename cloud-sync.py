import subprocess
import os
from datetime import datetime, timedelta
import sys

def sync_directory_to_cloud(local_directory : str, cloud_destination : str, extra_args : list = None):
    """
    Syncs a local directory to a cloud storage destination using rclone.

    Args:
    local_directory (str): Path to the local directory to be synced.
    cloud_destination (str): Remote destination in the cloud storage where the directory will be synced.
    extra_args (list): Extra arguments to pass to rclone calls.
    """
    # Construct the rclone sync command
    rclone_sync_command = ['rclone', 'bisync', local_directory, cloud_destination]
    if extra_args:
        rclone_sync_command.extend(extra_args)

    # Run the rclone sync command
    try:
        subprocess.run(rclone_sync_command, check=True)
        print("Sync completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing directory: {e}")

def backup_directory_to_cloud(local_directory : str, backup_destination : str, extra_args : list = None):
    """
    Backs up a local directory to a backup destination in the cloud.

    Args:
    local_directory (str): Path to the local directory to be backed up.
    backup_destination (str): Remote destination in the cloud storage where the backup will be stored.
    extra_args (list): Extra arguments to pass to rclone calls.
    """
    # Create a directory for today's backup
    today = datetime.now().strftime('%Y-%m-%d')
    backup_directory = os.path.join(backup_destination, today)

    # Construct the rclone sync command for backup
    rclone_backup_command = ['rclone', 'bisync', local_directory, backup_directory]
    if extra_args:
        rclone_backup_command.extend(extra_args)

    # Run the rclone backup command
    try:
        subprocess.run(rclone_backup_command, check=True)
        print("Backup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error backing up directory: {e}")

def rotate_backup(backup_destination : str, retention_period_days : int):
    """
    Rotates the backups to retain only the backups from the last 30 days.

    Args:
    backup_destination (str): Remote destination in the cloud storage where the backups are stored.
    """
    # Get the list of backup directories
    backup_directories = subprocess.check_output(['rclone', 'lsd', backup_destination]).decode('utf-8').split('\n')
    backup_directories = [d.split()[-1] for d in backup_directories if d]

    # Calculate the date 30 days ago
    thirty_days_ago = (datetime.now() - timedelta(days=retention_period_days)).strftime('%Y-%m-%d')

    # Delete backup directories older than 30 days
    for directory in backup_directories:
        if directory < thirty_days_ago:
            try:
                subprocess.run(['rclone', 'purge', os.path.join(backup_destination, directory)], check=True)
                print(f"Deleted backup directory: {directory}")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting backup directory {directory}: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python cloud-sync.py local_directory cloud_destination backup_destination retention_period_days [extra_args]")
        sys.exit(1)

    local_directory = sys.argv[1]
    cloud_destination = sys.argv[2]
    backup_destination = sys.argv[3]
    retention_period_days = sys.argv[4]

    extra_args = sys.argv[5:] if len(sys.argv) > 5 else None

    sync_directory_to_cloud(local_directory=local_directory, cloud_destination=cloud_destination, extra_args=extra_args)
    backup_directory_to_cloud(local_directory=local_directory, backup_destination=backup_destination, extra_args=extra_args)
    rotate_backup(backup_destination=backup_destination, retention_period_days=retention_period_days)
