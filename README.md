# KMusik

A simple CLI terminal music player for Linux. Point it at a folder of local audio files, pick a track from the list, and it plays using mpv.

## Features

- Scans a folder for MP3, FLAC, OGG, and M4A files
- Numbered track list in the terminal
- Pause, resume, stop, and quit from the keyboard
- Plays local music with no ads or accounts

## Requirements

- Python 3.8 or newer
- [mpv](https://mpv.io/) media player

Install mpv on Debian or Ubuntu:

```bash
sudo apt install mpv
```

## Usage

1. Make a music folder, for example `mkdir music`.
2. Add some songs to the folder.
3. Run the player with the folder path:

```bash
python3 kmusik.py "YOUR-FOLDER-DIRECTORY"
```

Type a track's number and press Enter to play it.

## Controls

Type a key and press Enter:

- `p` pause
- `s` stops playback
- `q` quits the player
- `r` resumes

## License

MIT. See [LICENSE](LICENSE).
