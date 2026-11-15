#!/bin/sh
set -e

SRC="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/.local/bin"
LINE='export PATH="$HOME/.local/bin:$PATH"'

if ! command -v mpv >/dev/null 2>&1; then
    echo "mpv is not installed. Install it first, for example:"
    echo "  sudo apt install mpv"
    exit 1
fi

mkdir -p "$BIN"
chmod +x "$SRC/kmusik"
ln -sf "$SRC/kmusik" "$BIN/kmusik"

case "$(basename "${SHELL:-}")" in
    zsh)  RC="$HOME/.zshrc" ;;
    fish) RC="" ;;
    *)    RC="$HOME/.bashrc" ;;
esac

case ":$PATH:" in
    *":$BIN:"*)
        ;; 
    *)
        if [ -z "$RC" ]; then
            echo "Add $BIN to your PATH manually (fish: fish_add_path $BIN)."
        elif grep -qsF "$LINE" "$RC"; then
            echo "PATH line already in $RC. Open a new terminal."
        else
            printf '\n# Added by KMusik installer\n%s\n' "$LINE" >> "$RC"
            echo "Added $BIN to your PATH in $RC."
            echo "Open a new terminal or run: source $RC"
        fi
        ;;
esac

echo "Installed. Run: kmusik ~/Music"
