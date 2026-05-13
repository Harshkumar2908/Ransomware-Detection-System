import os
import time

WATCH_FILE = "test_folder/test.txt"
LOCKED_FILE = "test_folder/test.txt.locked"

print("Auto Attack Simulator Started...")

while True:
    try:
        # Step 1: If locked file exists → restore it back
        if os.path.exists(LOCKED_FILE):
            os.rename(LOCKED_FILE, WATCH_FILE)
            print("Restored file for next attack...")

        # Step 2: Wait before attack
        time.sleep(2)

        # Step 3: Trigger attack (rename to .locked)
        if os.path.exists(WATCH_FILE):
            os.rename(WATCH_FILE, LOCKED_FILE)
            print("🚨 Attack Triggered!")

        else:
            print("File not found, waiting...")

        # Step 4: Wait before next cycle
        time.sleep(3)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)