# KMusik

A simple CLI terminal music player for Linux. Point it at a folder of local audio files, pick a track from the list, and it plays using mpv. No ads, no accounts.

## Features

- Scans a folder for MP3, FLAC, OGG, and M4A files
- Numbered track list in the terminal
- Pause, resume, stop, and quit from the keyboard
- Installs as a `kmusik` command you can run from any folder

## Requirements

- Linux
- Python 3.8 or newer
- [mpv](https://mpv.io/)

Install mpv on Debian or Ubuntu:

```bash
sudo apt install mpv
```

## Install

```bash
git clone https://github.com/Khayil98x95/KMusik.git
cd KMusik
./install.sh
```

Do not run the installer with `sudo`. It installs the command into your own `~/.local/bin` and adds that folder to your PATH if needed. Open a new terminal afterward (or run `source ~/.bashrc`).

## Usage

```bash
kmusik ~/Music
```

Type a track's number and press Enter to play it.

You can also run it without installing:

```bash
python3 kmusik.py ~/Music
```

## Controls

Type a key and press Enter:

| Key | Action |
|-----|--------|
| `p` | Pause or toggle playback |
| `r` | Resume playback |
| `s` | Stop playback |
| `q` | Quit |

## How it works

KMusik starts mpv as a background process with a control socket. The script reads your keys and sends commands to mpv through that socket, so mpv handles all the audio.

## Troubleshooting

- **`kmusik: command not found`:** open a new terminal, or run `source ~/.bashrc`.
- **`No audio files found`:** check the folder path. Folder names are case-sensitive on Linux (`Music` and `music` are different).
- **No sound or mpv errors:** confirm mpv works on its own with `mpv yourfile.mp3`.

## License

MIT. See [LICENSE](LICENSE).
