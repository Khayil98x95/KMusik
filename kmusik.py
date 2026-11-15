import subprocess
import os
import socket
import json
import sys
import time
import select
from pathlib import Path

SOCKET = "/tmp/music-player-mpv.sock"
AUDIO = {".mp3", ".flac", ".ogg", ".m4a"}
def send(command, wait_reply=True):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET)
            s.sendall((json.dumps({"command": command}) + "\n").encode())
            if wait_reply:
                return s.recv(4096).decode().strip()
    except OSError as err:
        print(f"[error] could not reach mpv: {err}")
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 kmusik.py ~/Music")
        return

    folder = Path(sys.argv[1]).expanduser()
    tracks = sorted(p for p in folder.iterdir() if p.suffix.lower() in AUDIO)

    if not tracks:
        print("No audio files found...")
        return

    for number, track in enumerate(tracks, start=1):
        print(f"[{number}]-{track.name}")
    while True:
        try:
            choice = int(input("Enter a number: "))
        except ValueError:
            print(f"Please choose a valid number from 1 to {len(tracks)}.")
            continue
        if 1 <= choice <= len(tracks):
            selected = tracks[choice - 1]
            break
        print(f"Please choose a number from 1 to {len(tracks)}")
   
    proc = subprocess.Popen([
        "mpv", "--no-video", f"--input-ipc-server={SOCKET}", str(selected)
        
    ])
    time.sleep(0.5)
    paused = False
    print("TIPS: P for Pause, R for Resume, S for Stop, and Q for Quit")
    try:
        while True:
            key = input("> ").strip().lower()
            if key == "p":
                send(["cycle", "pause"])
            elif key == "r":
                send(["set_property", "pause", False])
            elif key == "s":
                send(["stop"])
            elif key == "q":
                break
            elif key:
                print("Keys: p, r, s, q")
    except (KeyboardInterrupt, EOFError):
        print()

    if proc.poll() is None:
        send(["quit"], wait_reply=False)
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
        if os.path.exists(SOCKET):
            os.remove(SOCKET)

if __name__ == "__main__":
    main()
