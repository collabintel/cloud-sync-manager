import subprocess
import os
from datetime import datetime, timedelta
import sys

def download_from_cloud(local_directory : str, cloud_destination : str, extra_args : list = None):
    """
    Syncs a local directory to a cloud storage destination using rclone.

    Args:
    local_directory (str): Path to the local directory to be synced.
    cloud_destination (str): Remote destination in the cloud storage where the directory will be synced.
    extra_args (list): Extra arguments to pass to rclone calls.
    """
    # Construct the rclone sync command
    rclone_sync_command = ['rclone', 'sync', cloud_destination, local_directory]
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

    # Create the directory if it doesn't already exist.
    rclone_mkdir_command = ['rclone', 'mkdir', backup_directory]

    # Construct the rclone sync command for backup
    rclone_backup_command = ['rclone', 'sync', local_directory, backup_directory]
    if extra_args:
        rclone_backup_command.extend(extra_args)

    # Run the rclone backup command
    try:
        subprocess.run(rclone_mkdir_command, check=True)
        subprocess.run(rclone_backup_command, check=True)
        print("Backup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error backing up directory: {e}")

def rotate_backup(backup_destination : str, backup_retention : int):
    """
    Rotates the backups to retain only the amount of backups with given retention

    Args:
    backup_destination (str): Remote destination in the cloud storage where the backups are stored.
    backup_retention (int): The amount of backups permitted
    """
    # Get the list of backup directories
    backup_directories = subprocess.check_output(['rclone', 'lsd', backup_destination]).decode('utf-8').split('\n')
    backup_directories = [d.split()[-1] for d in backup_directories if d]

    if len(backup_directories) > backup_retention:
        # Delete backup directories more than the given backup retention
        amount_of_backups_to_remove = len(backup_directories) - backup_retention
        for backup_index in range(amount_of_backups_to_remove):
            directory = backup_directories[backup_index]
            try:
                subprocess.run(['rclone', 'purge', os.path.join(backup_destination, directory)], check=True)
                print(f"Deleted backup directory: {directory}")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting backup directory {directory}: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python cloud-sync.py local_directory cloud_destination backup_destination backup_retention [extra_args]")
        sys.exit(1)

    local_directory = sys.argv[1]
    cloud_destination = sys.argv[2]
    backup_destination = sys.argv[3]
    backup_retention = int(sys.argv[4])

    extra_args = sys.argv[5:] if len(sys.argv) > 5 else None

    backup_directory_to_cloud(local_directory=local_directory, backup_destination=backup_destination, extra_args=extra_args)
    rotate_backup(backup_destination=backup_destination, backup_retention=backup_retention)
    download_from_cloud(local_directory=local_directory, cloud_destination=cloud_destination, extra_args=extra_args)
