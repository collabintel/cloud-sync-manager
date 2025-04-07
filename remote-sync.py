import subprocess
import os
from datetime import datetime, timedelta
from argparse import ArgumentParser

def sync_directory_to_remote(local_directory : str, remote_destination : str, extra_args : list = None):
    """
    Syncs a local directory to a remote storage destination using rclone.

    Args:
    local_directory (str): Path to the local directory to be synced.
    remote_destination (str): Remote destination in the remote storage where the directory will be synced.
    extra_args (list): Extra arguments to pass to rclone calls.
    """
    # Construct the rclone sync command
    rclone_sync_command = ['rclone', 'bisync', remote_destination, local_directory]
    if extra_args:
        rclone_sync_command.extend(extra_args)

    # Run the rclone sync command
    try:
        subprocess.run(rclone_sync_command, check=True)
        print("Sync completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing directory: {e}")

def backup_directory_to_remote(local_directory : str, backup_destination : str, extra_args : list = None):
    """
    Backs up a local directory to a backup destination in the remote.

    Args:
    local_directory (str): Path to the local directory to be backed up.
    backup_destination (str): Remote destination in the remote storage where the backup will be stored.
    extra_args (list): Extra arguments to pass to rclone calls.
    """
    # Create a directory for today's backup
    today = datetime.now().strftime('%Y-%m-%d')
    backup_directory = os.path.join(backup_destination, today)

    # Create the directory if it doesn't already exist.
    rclone_mkdir_command = ['rclone', 'mkdir', backup_directory]

    # Construct the rclone sync command for backup
    rclone_backup_command = ['rclone', 'bisync', backup_directory, local_directory, '--resync']
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
    Rotates the backups to retain only the backups from the last 30 days.

    Args:
    backup_destination (str): Remote destination in the remote storage where the backups are stored.
    retention_period_days (int): The amount of days while the backups are being kept
    """
    # Get the list of backup directories
    backup_directories = subprocess.check_output(['rclone', 'lsd', backup_destination]).decode('utf-8').split('\n')
    backup_directories = [d.split()[-1] for d in backup_directories if d]

    # Calculate the retention period date
    retention_period_date = (datetime.now() - timedelta(days=backup_retention)).strftime('%Y-%m-%d')

    # Delete backup directories older than retention period date
    for directory in backup_directories:
        if directory < retention_period_date:
            try:
                subprocess.run(['rclone', 'purge', os.path.join(backup_destination, directory)], check=True)
                print(f"Deleted backup directory: {directory}")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting backup directory {directory}: {e}")

# Example usage
if __name__ == "__main__":
    parser = ArgumentParser(
        prog="download-from-remote",
        description="Download files from a remote location to your local directory"
    )

    parser.add_argument("--local-directory", action="store", type=str, required=True, help="Local directory to sync to")
    parser.add_argument("--remote-destination", action="store", type=str, required=True, help="Remote destination to sync from")
    parser.add_argument("--backup-destination", action="store", type=str, required=True, help="Backup destination to sync to")
    parser.add_argument("--backup-retention", action="store", type=int, default=7, help="Backup retention in days")
    parser.add_argument("--extra-args", action="append", help="Extra args to pass to rclone")

    cli_args = parser.parse_args()

    local_directory = cli_args.local_directory
    remote_destination = cli_args.remote_destination
    backup_destination = cli_args.backup_destination
    backup_retention = cli_args.backup_retention
    extra_args = cli_args.extra_args

    sync_directory_to_remote(local_directory=local_directory, remote_destination=remote_destination, extra_args=extra_args)
    backup_directory_to_remote(local_directory=local_directory, backup_destination=backup_destination, extra_args=extra_args)
    rotate_backup(backup_destination=backup_destination, backup_retention=backup_retention)
