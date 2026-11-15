#!/usr/bin/env python3
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
def get_prop(name):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect(SOCKET)
            request = {"command": ["get_property", name]}
            s.sendall((json.dumps(request) + "\n").encode())
            data = s.recv(4096).decode()
        for line in data.splitlines():
            msg = json.loads(line)
            if "error" in msg:
                return msg.get("data")
    except (OSError, ValueError):
        pass
    return None

def fmt(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}:{secs:02d}"


def draw_bar(width=30):
    pos = get_prop("time-pos")
    dur = get_prop("duration")
    if pos is None or not dur:
        return
    i = min(width - 1, int(width * pos / dur))
    bar = "-" * i + ">" + "-" * (width - i - 1)
    print(f"\r|{bar}| {fmt(pos)} / {fmt(dur)}  ", end="", flush=True)
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
    playlist = [str(t) for t in tracks[choice - 1:]]
    proc = subprocess.Popen([
        "mpv", "--no-video", "--idle", "--no-terminal", f"--input-ipc-server={SOCKET}", *playlist,
        
    ])
    time.sleep(0.5)
    paused = False
    print("TIPS: P for Pause, R for Resume, S for Stop, and Q for Quit")
    try:
        while proc.poll() is None:
            ready, _, _ = select.select([sys.stdin], [], [], 0.5)
            if ready:
                line = sys.stdin.readline()
                if line == "":
                    break
                key = line.strip().lower()
                if key == "p":
                    send(["cycle", "pause"])
                elif key == "r":
                    send(["set_property", "pause", False])
                elif key == "s":
                    send(["stop"])
                elif key == "q":
                    break
            draw_bar()
    except KeyboardInterrupt:
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
