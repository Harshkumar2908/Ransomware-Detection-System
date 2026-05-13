import time
import os
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
WATCH_FOLDER = os.path.join(BASE_DIR, "test_folder")
LOG_FILE = os.path.join(BASE_DIR, "logs", "logs.txt")
QUARANTINE_FOLDER = os.path.join(BASE_DIR, "quarantine")

class RansomwareHandler(FileSystemEventHandler):

    def on_modified(self, event):

        # Ignore directories
        if event.is_directory:
            return

        print(f"Modified: {event.src_path}")

        # Detect ransomware behavior (.locked file)
        if ".locked" in event.src_path:

            log_time = datetime.now().strftime("%H:%M:%S")

            warning = f"[{log_time}] WARNING: Possible Ransomware Attack Detected!"

            print(warning)
            print("Writing to log file...")
            print(LOG_FILE)

            try:
                # Ensure logs folder exists
                os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

                # Write log
                with open(LOG_FILE, "a") as file:
                    file.write(warning + "\n")

                # Ensure quarantine folder exists
                os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

                filename = os.path.basename(event.src_path)
                destination = os.path.join(QUARANTINE_FOLDER, filename)

                # Move file to quarantine (only if exists)
                if os.path.exists(event.src_path):

                    shutil.move(event.src_path, destination)

                    print("File moved to quarantine:", filename)

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":

    print("Monitoring Started...")
    with open("status.txt", "w") as f:
     f.write("running")

    event_handler = RansomwareHandler()
    observer = Observer()

    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:

     with open("status.txt", "w") as f:
        f.write("stopped")

    observer.stop()

    observer.join()