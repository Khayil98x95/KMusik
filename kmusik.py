import subprocess
import socket
import json
import sys
import time
from pathlib import Path

SOCKET = "/tmp/music-player-mpv.sock"
AUDIO = {".mp3", ".flac", ".ogg", ".m4a"}
def send(command):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET)
        s.sendall((json.dumps({"command": command}) + "\n").encode())

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

    choice = int(input("Enter a number: "))
    selected = tracks[choice - 1]
    
    proc = subprocess.Popen([
        "mpv", "--no-video", "--idle", f"--input-ipc-server={SOCKET}", str(selected)
        
    ])
    time.sleep(0.5)
    paused = False
    print("TIPS: P for Pause, R for Resume, S for Stop, and Q for Quit")
    while True:
        key = input(": ").strip().lower()
        print(f"[debug] got {key!r}")
        if key == "p":
            send(["cycle", "pause"])
        elif key == "s":
            send(["stop"])
        elif key == "r":
            send(["set_property", "pause", False])
        elif key == "q":
            send(["quit"])
            break

    proc.wait()

if __name__ == "__main__":
    main()
