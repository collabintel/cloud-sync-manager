import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="download-from-remote",
        description="Download files from a remote location to your local directory"
    )

    parser.add_argument("--local-directory", action="store", type=str, required=True, help="Local directory to sync")
    parser.add_argument("--remote-destination", action="store", type=str, required=True, help="Remote destination to sync to")
    parser.add_argument("--backup-destination", action="store", type=str, required=True, help="Backup destination to sync")
    parser.add_argument("--backup-retention", action="store", type=int, default=7, help="Backup retention in days")
    parser.add_argument("--extra-args", action="append", help="Extra args to pass to rclone")

    cli_args = parser.parse_args()

    print(cli_args.local_directory)
    print(cli_args.remote_destination)
    print(cli_args.backup_destination)
    print(cli_args.backup_retention)
    print(cli_args.extra_args)


# # Example usage
# if __name__ == "__main__":
#     if len(sys.argv) < 5:
#         print("Usage: python cloud-sync.py local_directory cloud_destination backup_destination backup_retention [extra_args]")
#         sys.exit(1)

#     local_directory = sys.argv[1]
#     cloud_destination = sys.argv[2]
#     backup_destination = sys.argv[3]
#     backup_retention = int(sys.argv[4])

#     extra_args = sys.argv[5:] if len(sys.argv) > 5 else None
