# Cloud Sync Manager

Uses rclone to sync a local directory with a cloud location. Also backups to an another directory in the cloud, creates directories for every day rotates the backup for the given retention period.

Parameters:

* local_directory: local directory in your pc to sync with cloud
* cloud_destination: cloud destination(including the directory) to sync with your local directory
* backup_destination: backup destination(including the directory) to sync with your local directory
* retention_period_days: how many days you want to keep your backups
