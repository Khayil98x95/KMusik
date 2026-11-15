#!/bin/sh
set -e

SRC="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/.local/bin"

if ! command -v mpv >/dev/null 2>&1; then
    echo "mpv is not installed. Install it first, for example:"
    echo "  sudo apt install mpv"
    exit 1
fi

mkdir -p "$BIN"
chmod +x "$SRC/kmusik"
ln -sf "$SRC/kmusik" "$BIN/kmusik"

echo "Installed. Run: kmusik ~/Music"

case ":$PATH:" in
    *":$BIN:"*) ;;
    *) echo "Add this line to ~/.bashrc, then open a new terminal:"
       echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"" ;;
esac
